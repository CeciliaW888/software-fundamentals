from __future__ import annotations

import ast
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
        self.code_blocks: list[str] = []
        self._in_title = False
        self._in_pre = False
        self._in_pre_code = False
        self._code_buffer: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attributes = dict(attrs)
        if tag == "title":
            self._in_title = True
        if tag == "pre":
            self._in_pre = True
        if tag == "code" and self._in_pre:
            self._in_pre_code = True
            self._code_buffer = []
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
        if tag == "code" and self._in_pre_code:
            self.code_blocks.append("".join(self._code_buffer))
            self._in_pre_code = False
        if tag == "pre":
            self._in_pre = False

    def handle_data(self, data: str) -> None:
        if self._in_title:
            self.title += data
        if self._in_pre_code:
            self._code_buffer.append(data)


def verify_document(path: Path) -> list[str]:
    errors: list[str] = []
    parser = DocumentParser()
    parser.feed(path.read_text(encoding="utf-8"))
    if not parser.title.strip():
        errors.append(f"{path}: missing title")
    if parser.heading_count < 2:
        errors.append(f"{path}: expected at least two headings")
    for block_index, code in enumerate(parser.code_blocks, start=1):
        try:
            ast.parse(code)
        except SyntaxError as error:
            errors.append(f"{path}: Python block {block_index} has invalid syntax: {error.msg} at line {error.lineno}")
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
