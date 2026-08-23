from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
HTML_FILES = [ROOT / "index.html"] + sorted((ROOT / "lessons").glob("*.html")) + sorted((ROOT / "reference").glob("*.html"))


class DocumentParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.title = ""
        self.heading_count = 0
        self.links: list[str] = []
        self.scripts: list[str] = []
        self._in_title = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attributes = dict(attrs)
        if tag == "title":
            self._in_title = True
        if tag in {"h1", "h2", "h3"}:
            self.heading_count += 1
        if tag == "a" and attributes.get("href"):
            self.links.append(attributes["href"] or "")
        if tag == "link" and attributes.get("href"):
            self.links.append(attributes["href"] or "")
        if tag == "script" and attributes.get("src"):
            self.scripts.append(attributes["src"] or "")

    def handle_endtag(self, tag: str) -> None:
        if tag == "title":
            self._in_title = False

    def handle_data(self, data: str) -> None:
        if self._in_title:
            self.title += data


def verify_document(path: Path) -> list[str]:
    errors: list[str] = []
    parser = DocumentParser()
    parser.feed(path.read_text(encoding="utf-8"))
    if not parser.title.strip():
        errors.append(f"{path}: missing title")
    if parser.heading_count < 2:
        errors.append(f"{path}: expected at least two headings")
    for target in parser.links + parser.scripts:
        if target.startswith(("http://", "https://", "data:", "#", "mailto:")):
            continue
        local_path = (path.parent / target).resolve()
        if not local_path.exists():
            errors.append(f"{path}: broken local reference {target}")
    return errors


def main() -> int:
    if not HTML_FILES:
        print("No HTML artifacts found", file=sys.stderr)
        return 1
    errors = [error for path in HTML_FILES for error in verify_document(path)]
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print(f"verified_html={len(HTML_FILES)}")
    print("broken_local_references=0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
