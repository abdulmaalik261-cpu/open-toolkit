from pathlib import Path

from open_toolkit.commands.diagram import build_graph, to_mermaid


def test_build_graph_detects_local_import(tmp_path: Path):
    (tmp_path / "a.py").write_text("import b\n")
    (tmp_path / "b.py").write_text("x = 1\n")

    graph = build_graph(tmp_path)
    assert "a" in graph
    assert "b" in graph["a"]


def test_to_mermaid_contains_edge():
    graph = {"a": {"b"}, "b": set()}
    out = to_mermaid(graph)
    assert "graph TD" in out
    assert "a --> b" in out


def test_to_mermaid_handles_empty_graph():
    out = to_mermaid({})
    assert "No internal imports found" in out
