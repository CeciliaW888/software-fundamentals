"""Check the course content against the practice project.

    python3 scripts/check_course.py           # code and local links
    python3 scripts/check_course.py --links   # also fetch every external link

Checks:
1. Every Python block in the guides and website modules parses.
2. Every Python or SQL block in a guide is preceded by a File marker,
   *File: [`projects/...`](...)*, and matches that file:
   - Python: each top-level statement in the snippet equals a statement
     somewhere in the file (compared as syntax trees, so formatting and
     docstrings do not matter). A function whose body is only `...` is
     checked by its signature. A class is checked method by method.
   - SQL: the snippet, with whitespace collapsed, appears in the file.
3. Relative links in Markdown files point at files that exist.
4. With --links, every external link answers with HTTP status below 400.
"""
from __future__ import annotations

import ast
import html
import re
import sys
import textwrap
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FILE_MARKER = re.compile(r"^\*File: \[`([^`]+)`\]\(([^)]+)\)\*$")
FENCE = re.compile(r"```(\w*)\n(.*?)```", re.S)


def strip_docstrings(tree: ast.AST) -> ast.AST:
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef, ast.Module)):
            body = node.body
            if body and isinstance(body[0], ast.Expr) and isinstance(getattr(body[0], "value", None), ast.Constant) \
                    and isinstance(body[0].value.value, str):
                node.body = body[1:] or [ast.Pass()]
    return tree


def is_ellipsis(node: ast.AST) -> bool:
    return isinstance(node, ast.Expr) and isinstance(node.value, ast.Constant) and node.value.value is Ellipsis


def signature(node: ast.AST) -> str:
    return ast.dump(node.args) + node.name


def statement_matches(snippet: ast.stmt, candidates: list[ast.stmt]) -> bool:
    if is_ellipsis(snippet):
        return True
    if isinstance(snippet, (ast.FunctionDef, ast.AsyncFunctionDef)):
        body = [s for s in snippet.body if not isinstance(s, ast.Pass)]
        same_name = [c for c in candidates if isinstance(c, type(snippet)) and c.name == snippet.name]
        if all(is_ellipsis(s) for s in body):
            return any(signature(c) == signature(snippet) for c in same_name)
        return any(ast.dump(c) == ast.dump(snippet) for c in same_name)
    if isinstance(snippet, ast.ClassDef):
        for candidate in candidates:
            if isinstance(candidate, ast.ClassDef) and candidate.name == snippet.name:
                inner = list(ast.walk(candidate))
                inner_statements = [n for n in inner if isinstance(n, ast.stmt) and n is not candidate]
                return all(statement_matches(s, inner_statements) for s in snippet.body if not isinstance(s, ast.Pass))
        return False
    dumped = ast.dump(snippet)
    return any(ast.dump(c) == dumped for c in candidates)


def python_matches(snippet: str, source: str) -> list[str]:
    snippet_tree = strip_docstrings(ast.parse(textwrap.dedent(snippet)))
    file_tree = strip_docstrings(ast.parse(source))
    candidates = [n for n in ast.walk(file_tree) if isinstance(n, ast.stmt)]
    return [ast.unparse(s).splitlines()[0] for s in snippet_tree.body if not statement_matches(s, candidates)]


def squash(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def check_guides(problems: list[str]) -> int:
    checked = 0
    for guide in sorted(ROOT.glob("week-*/day-*.md")):
        lines = guide.read_text().splitlines()
        text = "\n".join(lines)
        for match in FENCE.finditer(text):
            language, body = match.group(1), match.group(2)
            if language not in ("python", "sql"):
                continue
            before = text[: match.start()].rstrip().splitlines()
            marker = FILE_MARKER.match(before[-1].strip()) if before else None
            where = f"{guide.relative_to(ROOT)}: block starting {body.strip().splitlines()[0][:60]!r}"
            if language == "python":
                try:
                    ast.parse(textwrap.dedent(body))
                except SyntaxError as error:
                    problems.append(f"{where}: does not parse ({error})")
                    continue
            if not marker:
                problems.append(f"{where}: no *File: [...]* marker above it")
                continue
            source_path = ROOT / marker.group(1)
            if not source_path.exists():
                problems.append(f"{where}: {marker.group(1)} does not exist")
                continue
            expected_link = Path(marker.group(2))
            if (guide.parent / expected_link).resolve() != source_path.resolve():
                problems.append(f"{where}: marker link {marker.group(2)} does not point at {marker.group(1)}")
            source = source_path.read_text()
            if language == "python":
                missing = python_matches(body, source)
                if missing:
                    problems.append(f"{where}: not found in {marker.group(1)}: {missing}")
            elif squash(body) not in squash(source):
                problems.append(f"{where}: SQL not found in {marker.group(1)}")
            checked += 1
    return checked


def check_modules(problems: list[str]) -> int:
    parsed = 0
    for module in sorted(ROOT.glob("website/modules/*.html")):
        for block in re.findall(r'data-lang="python".*?<pre><code>(.*?)</code></pre>', module.read_text(), re.S):
            try:
                ast.parse(textwrap.dedent(html.unescape(block)))
                parsed += 1
            except SyntaxError as error:
                problems.append(f"{module.relative_to(ROOT)}: Python block does not parse ({error})")
    return parsed


def markdown_files() -> list[Path]:
    return [p for p in ROOT.rglob("*.md") if ".venv" not in p.parts and ".git" not in p.parts and "artifacts" not in p.parts]


def check_relative_links(problems: list[str]) -> None:
    for path in markdown_files():
        text = re.sub(r"```.*?```", "", path.read_text(), flags=re.S)
        for target in re.findall(r"\]\(([^)#\s]+)(?:#[^)]*)?\)", text):
            if target.startswith(("http://", "https://", "mailto:")):
                continue
            if not (path.parent / target).exists():
                problems.append(f"{path.relative_to(ROOT)}: broken relative link {target}")


def external_links() -> set[str]:
    files = markdown_files() + list(ROOT.glob("website/**/*.html"))
    links = set()
    for path in files:
        for url in re.findall(r"https?://[^\s)\"'<>`]+", path.read_text()):
            url = url.rstrip(".,;")
            if "localhost" in url or ".example" in url or "fonts.g" in url or "img.shields.io" in url:
                continue
            links.add(html.unescape(url))
    return links


def fetch_status(url: str) -> tuple[str, int | str]:
    request = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (course link check)"})
    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            return url, response.status
    except urllib.error.HTTPError as error:
        return url, error.code
    except Exception as error:  # report, do not crash, on any network problem
        return url, type(error).__name__


def check_external_links(problems: list[str]) -> int:
    links = sorted(external_links())
    with ThreadPoolExecutor(max_workers=8) as pool:
        for url, status in pool.map(fetch_status, links):
            if not isinstance(status, int) or status >= 400:
                problems.append(f"external link {url}: {status}")
    return len(links)


def main() -> int:
    problems: list[str] = []
    snippets = check_guides(problems)
    module_blocks = check_modules(problems)
    check_relative_links(problems)
    summary = f"{snippets} guide snippets matched the project, {module_blocks} module Python blocks parsed"
    if "--links" in sys.argv:
        summary += f", {check_external_links(problems)} external links checked"
    for problem in problems:
        print("✗", problem)
    print(("✗ " if problems else "✓ ") + summary + (f", {len(problems)} problems" if problems else ""))
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
