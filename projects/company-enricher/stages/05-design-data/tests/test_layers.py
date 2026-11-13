"""Day 15: the core never imports adapters, so the core can be read and changed alone."""
import ast
from pathlib import Path

CORE = Path(__file__).resolve().parents[1] / "enricher" / "core"


def imported_modules(path):
    tree = ast.parse(path.read_text())
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module:
            yield node.module
        elif isinstance(node, ast.Import):
            yield from (alias.name for alias in node.names)


def test_core_does_not_import_adapters():
    offenders = {
        path.name: module
        for path in CORE.glob("*.py")
        for module in imported_modules(path)
        if module.startswith("enricher.adapters")
    }
    assert offenders == {}
