"""
toolkit diagram — walk a Python codebase and emit a Mermaid dependency
diagram of which modules import which. Works as a plain CLI, and the
same logic is exposed as a Claude Skill (see skill/diagram/SKILL.md)
so an AI agent can call it as a tool.
"""
from __future__ import annotations

import ast
import sys
from pathlib import Path
from typing import Dict, Set


def _module_name(path: Path, root: Path) -> str:
    rel = path.relative_to(root).with_suffix("")
    parts = [p for p in rel.parts if p != "__init__"]
    return ".".join(parts) if parts else path.stem


def _local_modules(root: Path) -> Dict[str, Path]:
    mapping = {}
    for py in root.rglob("*.py"):
        if any(part.startswith(".") for part in py.parts):
            continue
        mapping[_module_name(py, root)] = py
    return mapping


def _imports_of(py_file: Path) -> Set[str]:
    try:
        tree = ast.parse(py_file.read_text(encoding="utf-8", errors="ignore"))
    except SyntaxError:
        return set()
    found = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                found.add(alias.name.split(".")[0])
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                found.add(node.module.split(".")[0])
    return found


def build_graph(root: Path) -> Dict[str, Set[str]]:
    modules = _local_modules(root)
    top_level = {name.split(".")[0] for name in modules}
    graph: Dict[str, Set[str]] = {}
    for name, path in modules.items():
        top = name.split(".")[0]
        edges = {imp for imp in _imports_of(path) if imp in top_level and imp != top}
        graph.setdefault(top, set())
        graph[top] |= edges
    return graph


def to_mermaid(graph: Dict[str, Set[str]]) -> str:
    lines = ["graph TD"]
    seen_nodes = set()
    for node in graph:
        if node not in seen_nodes:
            lines.append(f'    {node}["{node}"]')
            seen_nodes.add(node)
    for src, targets in graph.items():
        for dst in sorted(targets):
            lines.append(f"    {src} --> {dst}")
    if len(lines) == 1:
        lines.append("    empty[\"No internal imports found\"]")
    return "\n".join(lines)


def run(args) -> int:
    root = Path(args.path).resolve()
    if not root.exists():
        print(f"error: path not found: {root}", file=sys.stderr)
        return 1
    graph = build_graph(root)
    mermaid = to_mermaid(graph)

    if args.output:
        out_path = Path(args.output)
        if out_path.suffix == ".md":
            out_path.write_text(f"```mermaid\n{mermaid}\n```\n", encoding="utf-8")
        else:
            out_path.write_text(mermaid, encoding="utf-8")
        print(f"Wrote diagram to {out_path}")
    else:
        print(mermaid)
    return 0


def add_subparser(subparsers):
    p = subparsers.add_parser(
        "diagram",
        help="Generate a Mermaid dependency diagram for a Python codebase",
        description="Walks a directory of .py files and emits a Mermaid graph "
        "of top-level-package import relationships.",
    )
    p.add_argument("path", nargs="?", default=".", help="Path to the codebase (default: current dir)")
    p.add_argument("-o", "--output", help="Write output to a file (.md wraps it in a fenced code block)")
    p.set_defaults(func=run)
