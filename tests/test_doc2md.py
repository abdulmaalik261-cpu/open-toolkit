import pytest

from open_toolkit.commands.doc2md import convert


def test_unsupported_extension_raises(tmp_path):
    f = tmp_path / "file.xyz"
    f.write_text("hello")
    with pytest.raises(ValueError):
        convert(str(f))


def test_missing_file_raises(tmp_path):
    with pytest.raises(FileNotFoundError):
        convert(str(tmp_path / "nope.pdf"))


def test_txt_passthrough(tmp_path):
    f = tmp_path / "file.txt"
    f.write_text("hello world")
    assert convert(str(f)) == "hello world"


def test_html_file_to_markdown(tmp_path):
    f = tmp_path / "file.html"
    f.write_text("<h1>Title</h1><p>Body text</p>")
    out = convert(str(f))
    assert "Title" in out
    assert "Body text" in out
