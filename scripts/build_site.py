"""Build the website data from the daily Markdown guides.

    python3 scripts/build_site.py

The Markdown guide in week-NN/ is the single source for each day. This
script writes, for every day:

- website/modules/NN-slug.html  the lazy-loaded lesson fragment
- website/data/quiz-NN.json     the day's "Check" questions
- website/data/flashcards.json  every Key Terminology row, with its source

Days listed in HAND_WRITTEN_MODULES keep their hand-made module and quiz
(they use custom exercises), but still contribute flashcards.

Only the Markdown subset used by the guides is supported: headings,
paragraphs, lists, task lists, tables, fenced code, blockquotes,
<details>, and inline bold, italic, code and links.
"""
from __future__ import annotations

import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CURRENT_GUIDE_DIR = ROOT / "week-01"  # set per guide in build_day, so relative links resolve from it
REPO_URL = "https://github.com/CeciliaW888/software-fundamentals"
HAND_WRITTEN_MODULES = {1, 2}

FILE_MARKER = re.compile(r"^\*File: \[`([^`]+)`\]\(([^)]+)\)\*$")
QUESTION = re.compile(r"^\*\*Q(\d+)\. (.+)\*\*$")
OPTION = re.compile(r"^- ([A-E])\. (.+)$")
ANSWER = re.compile(r"^\*\*([A-E])\.\*\* (.+)$", re.S)


# ── Inline Markdown ──────────────────────────────────────────────────────────

def inline(text: str) -> str:
    """Render inline Markdown to HTML. Code spans are protected first."""
    codes: list[str] = []

    def keep_code(match):
        codes.append(f"<code>{html.escape(match.group(1), quote=False)}</code>")
        return f"\x00{len(codes) - 1}\x00"

    text = re.sub(r"`([^`]+)`", keep_code, text)
    text = html.escape(text, quote=False)
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", lambda m: link(m.group(1), m.group(2)), text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?!\w)", r"<em>\1</em>", text)
    return re.sub(r"\x00(\d+)\x00", lambda m: codes[int(m.group(1))], text)


def link(label: str, target: str) -> str:
    """Relative links point at the repo on GitHub, since the site only serves website/."""
    if not target.startswith(("http://", "https://", "#")):
        resolved = (CURRENT_GUIDE_DIR / target).resolve()
        try:
            relative = resolved.relative_to(ROOT)
        except ValueError:
            relative = Path(target)
        kind = "tree" if resolved.is_dir() else "blob"
        target = f"{REPO_URL}/{kind}/main/{relative.as_posix()}"
    return f'<a href="{html.escape(target)}" target="_blank" rel="noopener">{label}</a>'


def plain(text: str) -> str:
    """Inline Markdown to plain text, for JSON data."""
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    return re.sub(r"[*`]", "", text).strip()


# ── Block parsing ────────────────────────────────────────────────────────────

def blocks(lines: list[str]):
    """Yield (kind, payload) blocks from Markdown lines."""
    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        if not stripped or stripped == "---":
            i += 1
        elif stripped.startswith("```"):
            language = stripped[3:].strip()
            body = []
            i += 1
            while not lines[i].strip().startswith("```"):
                body.append(lines[i])
                i += 1
            yield "code", (language, "\n".join(body))
            i += 1
        elif stripped.startswith("<details"):
            depth, body = 1, []
            i += 1
            while depth:
                if lines[i].strip().startswith("<details"):
                    depth += 1
                if lines[i].strip() == "</details>":
                    depth -= 1
                    if not depth:
                        break
                body.append(lines[i])
                i += 1
            summary = re.search(r"<summary>(.*?)</summary>", "\n".join(body))
            inner = [l for l in body if "<summary>" not in l]
            yield "details", (summary.group(1) if summary else "Details", inner)
            i += 1
        elif stripped.startswith("#"):
            level = len(stripped) - len(stripped.lstrip("#"))
            yield "heading", (level, stripped[level:].strip())
            i += 1
        elif stripped.startswith(">"):
            body = []
            while i < len(lines) and lines[i].strip().startswith(">"):
                body.append(lines[i].strip()[1:].strip())
                i += 1
            yield "quote", " ".join(b for b in body if b)
        elif stripped.startswith("|"):
            rows = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                rows.append([c.strip() for c in lines[i].strip().strip("|").split("|")])
                i += 1
            yield "table", rows
        elif re.match(r"^(- |\d+\. )", stripped):
            ordered = bool(re.match(r"^\d+\. ", stripped))
            items: list[str] = []
            while i < len(lines) and (re.match(r"^(- |\d+\. )", lines[i].strip()) or lines[i].startswith("   ")):
                if lines[i].startswith("   ") and items:
                    items[-1] += "\n" + lines[i].strip()
                else:
                    items.append(re.sub(r"^(- |\d+\. )", "", lines[i].strip()))
                i += 1
            yield "list", (ordered, items)
        else:
            body = []
            while i < len(lines) and lines[i].strip() and not re.match(r"^(#|>|\||```|<details|- |\d+\. )", lines[i].strip()):
                body.append(lines[i].strip())
                i += 1
            yield "paragraph", body


# ── Rendering ────────────────────────────────────────────────────────────────

class Renderer:
    def __init__(self, terms: dict[str, str]):
        self.terms = terms
        self.used_terms: set[str] = set()
        self.quiz: list[dict] = []
        self.pending_file: tuple[str, str] | None = None
        self.pending_question: dict | None = None

    def tooltip(self, rendered: str) -> str:
        """Wrap the first use of each key term in a sourced tooltip."""
        for term, definition in self.terms.items():
            if term in self.used_terms:
                continue
            pattern = re.compile(rf"(?<![\w-])({re.escape(term)}s?)(?![\w-])", re.I)
            parts = re.split(r"(<[^>]+>)", rendered)
            inside = 0
            for index, part in enumerate(parts):
                if part.startswith("<"):
                    if re.match(r"<(code|a)\b", part):
                        inside += 1
                    elif re.match(r"</(code|a)>", part):
                        inside -= 1
                    continue
                if inside:
                    continue
                match = pattern.search(part)
                if match:
                    span = (f'<span class="term" tabindex="0" data-definition="{html.escape(definition)}">'
                            f"{match.group(1)}</span>")
                    parts[index] = part[: match.start()] + span + part[match.end():]
                    self.used_terms.add(term)
                    break
            rendered = "".join(parts)
        return rendered

    def render(self, lines: list[str], in_core: bool = False) -> list[str]:
        out: list[str] = []
        section = ""
        for kind, payload in blocks(lines):
            if kind == "heading":
                level, text = payload
                section = text if level == 2 else section
                in_core = "Core Concepts" in section
                if level == 1:
                    continue
                tag = {2: "h3", 3: "h4"}.get(level, "h4")
                out.append(f"<{tag}>{inline(text)}</{tag}>")
            elif kind == "paragraph":
                text = " ".join(payload)
                hard_breaks = any(line.endswith("\\") for line in payload)
                if re.match(r"^\[.*Course Home", text):
                    continue
                file_marker = FILE_MARKER.match(text)
                question = QUESTION.match(text)
                if file_marker:
                    self.pending_file = (file_marker.group(1), file_marker.group(2))
                    continue
                if question:
                    self.pending_question = {"question": plain(question.group(2)), "html": inline(question.group(2)), "options": []}
                    continue
                rendered = inline(text) if not hard_breaks else "<br>".join(inline(line.rstrip("\\").strip()) for line in payload)
                if in_core or "Code Examples" in section:
                    rendered = self.tooltip(rendered)
                out.append(f"<p>{rendered}</p>")
            elif kind == "quote":
                out.append(self.callout(payload))
            elif kind == "table" and "Key Terminology" in section:
                out.append(self.term_cards(payload))
            elif kind == "table":
                rendered = self.table(payload)
                out.append(self.tooltip(rendered) if in_core else rendered)
            elif kind == "list":
                ordered, items = payload
                if self.pending_question is not None and all(OPTION.match(f"- {item}") for item in items):
                    self.pending_question["options"] = [OPTION.match(f"- {item}").group(2) for item in items]
                    continue
                rendered = self.list(ordered, items)
                out.append(self.tooltip(rendered) if in_core else rendered)
            elif kind == "code":
                out.append(self.code(*payload))
            elif kind == "details":
                summary, inner = payload
                if self.pending_question is not None and summary.strip() == "Answer":
                    out.append(self.quiz_card(inner))
                    continue
                body = "\n".join(self.render(inner, in_core))
                out.append(f'<details class="exercise-hints"><summary>{inline(summary)}</summary>{body}</details>')
        return out

    def callout(self, text: str) -> str:
        if text.startswith("📍"):
            body = text.removeprefix("📍").strip()
            return f'<div class="callout-accent"><span class="callout-icon">📍</span><div class="callout-content">{inline(body)}</div></div>'
        if text.startswith("**Key Insight:**"):
            return f'<div class="callout-accent"><span class="callout-icon">💡</span><div class="callout-content">{inline(text)}</div></div>'
        if text.startswith("**Warning") or text.startswith("**Book source TBC"):
            return f'<div class="callout-warning"><span class="callout-icon">⚠️</span><div class="callout-content">{inline(text)}</div></div>'
        return f'<div class="callout-info"><span class="callout-icon">ℹ️</span><div class="callout-content">{inline(text)}</div></div>'

    def table(self, rows: list[list[str]]) -> str:
        header, body = rows[0], [r for r in rows[2:]]
        head = "".join(f"<th>{inline(c)}</th>" for c in header)
        rows_html = "".join("<tr>" + "".join(f"<td>{self.cell(c)}</td>" for c in r) + "</tr>" for r in body)
        return f"<table><thead><tr>{head}</tr></thead><tbody>{rows_html}</tbody></table>"

    @staticmethod
    def term_cards(rows: list[list[str]]) -> str:
        """Key Terminology as the skill's term cards, which read better on phones than a 3-column table."""
        cards = "".join(
            f'<div class="term-card"><dt>{inline(term)}</dt><dd>{inline(definition)}<br><em>{inline(source)}</em></dd></div>'
            for term, definition, source in rows[2:]
        )
        return f'<dl class="term-grid">{cards}</dl>'

    @staticmethod
    def cell(text: str) -> str:
        rendered = inline(text)
        # Long identifiers may break after an underscore on phones.
        return re.sub(r"<code>([^<]+)</code>", lambda m: "<code>" + m.group(1).replace("_", "_<wbr>") + "</code>", rendered)

    def list(self, ordered: bool, items: list[str]) -> str:
        if all(item.startswith("[ ] ") for item in items):
            labels = "".join(f'<label><input type="checkbox"> {inline(item[4:])}</label>' for item in items)
            return f'<div class="checklist">{labels}</div>'
        tag = "ol" if ordered else "ul"
        rendered = []
        for item in items:
            first, *rest = item.split("\n")
            extra = "".join(f"<br>{inline(line.removeprefix('- '))}" for line in rest)
            rendered.append(f"<li>{inline(first)}{extra}</li>")
        return f"<{tag}>{''.join(rendered)}</{tag}>"

    def code(self, language: str, body: str) -> str:
        label = language or "text"
        if self.pending_file:
            path, _ = self.pending_file
            label = path.split("stages/", 1)[-1]
            stage, _, rest = label.partition("/")
            if stage[:2].isdigit():
                label = f"stage {stage[:2]} · {rest}"
            self.pending_file = None
        return (
            f'<div class="code-block" data-lang="{html.escape(language)}">'
            f'<div class="code-header"><span class="filename">{html.escape(label)}</span>'
            '<button class="copy-btn" onclick="copyCode(this)">📋 Copy</button></div>'
            f"<pre><code>{html.escape(body, quote=False)}</code></pre></div>"
        )

    def quiz_card(self, answer_lines: list[str]) -> str:
        question = self.pending_question
        self.pending_question = None
        answer_text = " ".join(l.strip() for l in answer_lines if l.strip())
        match = ANSWER.match(answer_text)
        if not match or not question["options"]:
            raise ValueError(f"Malformed quiz question: {question['question']}")
        correct = "ABCDE".index(match.group(1))
        explanation = plain(match.group(2))
        self.quiz.append({
            "question": question["question"],
            "options": [plain(o) for o in question["options"]],
            "answer": correct,
            "explanation": explanation,
        })
        buttons = []
        for index, option in enumerate(question["options"]):
            if index == correct:
                attrs = f'data-correct="true" data-explanation-correct="{html.escape("Correct. " + explanation)}"'
            else:
                attrs = f'data-correct="false" data-explanation-wrong="{html.escape(f"Not quite: the answer is {match.group(1)}. " + explanation)}"'
            buttons.append(f'<button class="quiz-option" {attrs}>{inline(option)}</button>')
        number = len(self.quiz)
        return (f'<div class="quiz-card"><p class="quiz-question"><strong>Q{number}:</strong> {question["html"]}</p>'
                f'<div class="quiz-options">{"".join(buttons)}</div></div>')


# ── Days ─────────────────────────────────────────────────────────────────────

def guides() -> list[Path]:
    return sorted(ROOT.glob("week-*/day-*.md"), key=lambda p: int(p.name[4:6]))


def key_terms(text: str) -> list[tuple[str, str, str]]:
    if "## 🔑 Key Terminology" not in text:
        return []
    section = text.split("## 🔑 Key Terminology", 1)[1].split("\n## ", 1)[0]
    rows = []
    for line in section.splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if line.startswith("|") and len(cells) >= 3 and cells[0] not in ("Term",) and not set(cells[0]) <= set("-: "):
            rows.append((plain(cells[0]), plain(cells[1]), plain(cells[2])))
    return rows


def build_day(path: Path, flashcards: dict[str, dict]) -> None:
    global CURRENT_GUIDE_DIR
    CURRENT_GUIDE_DIR = path.parent
    day = int(path.name[4:6])
    text = path.read_text()
    terms = key_terms(text)
    for term, definition, source in terms:
        flashcards.setdefault(term.lower(), {"term": term, "definition": f"{definition} Source: {source.rstrip('.')}."})
    if day in HAND_WRITTEN_MODULES or "Status: Outline" in text:
        return

    title = text.splitlines()[0].split(":", 1)[1].strip()
    tooltip_terms = {term: f"{definition} Source: {source.rstrip('.')}." for term, definition, source in terms}
    renderer = Renderer(tooltip_terms)
    body = "\n    ".join(renderer.render(text.splitlines()))
    guide_url = f"{REPO_URL}/blob/main/{path.relative_to(ROOT).as_posix()}"
    module = (
        f'<section class="module" id="module-{day}" data-day="{day}">\n'
        f'  <div class="module-inner">\n'
        f"    <h2>{html.escape(title)}</h2>\n"
        f"    {body}\n"
        f'    <p><a href="{guide_url}" target="_blank" rel="noopener">Read this guide as Markdown on GitHub →</a></p>\n'
        f"  </div>\n</section>\n"
    )
    slug = path.stem.split("-", 2)[2]
    (ROOT / f"website/modules/{day:02d}-{slug}.html").write_text(module)
    if len(renderer.quiz) < 3:
        raise ValueError(f"Day {day} has {len(renderer.quiz)} quiz questions; the skill needs 3 or more")
    quiz = {"day": day, "title": title, "questions": renderer.quiz}
    (ROOT / f"website/data/quiz-{day:02d}.json").write_text(json.dumps(quiz, indent=2, ensure_ascii=False) + "\n")


def main() -> int:
    flashcards: dict[str, dict] = {}
    for path in guides():
        build_day(path, flashcards)
    (ROOT / "website/data/flashcards.json").write_text(json.dumps(list(flashcards.values()), indent=2, ensure_ascii=False) + "\n")
    print(f"Built {len(guides())} days, {len(flashcards)} flashcards")
    return 0


if __name__ == "__main__":
    sys.exit(main())
