"""
toolkit doc2md — convert a PDF, DOCX, HTML file, or a URL into clean
Markdown with a single command.
"""
from __future__ import annotations

import sys
from pathlib import Path
from urllib.parse import urlparse


def _from_pdf(path: Path) -> str:
    from pypdf import PdfReader

    reader = PdfReader(str(path))
    parts = []
    for i, page in enumerate(reader.pages):
        text = (page.extract_text() or "").strip()
        if text:
            parts.append(f"<!-- page {i + 1} -->\n\n{text}")
    return "\n\n".join(parts) + "\n"


def _from_docx(path: Path) -> str:
    import docx

    document = docx.Document(str(path))
    lines = []
    for para in document.paragraphs:
        text = para.text.strip()
        if not text:
            continue
        style = (para.style.name or "").lower()
        if style.startswith("heading 1"):
            lines.append(f"# {text}")
        elif style.startswith("heading 2"):
            lines.append(f"## {text}")
        elif style.startswith("heading 3"):
            lines.append(f"### {text}")
        elif style.startswith("list"):
            lines.append(f"- {text}")
        else:
            lines.append(text)
    return "\n\n".join(lines) + "\n"


def _html_to_md(html: str) -> str:
    from bs4 import BeautifulSoup
    from markdownify import markdownify

    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(["script", "style", "nav", "footer", "noscript"]):
        tag.decompose()
    return markdownify(str(soup), heading_style="ATX").strip() + "\n"


def _from_html_file(path: Path) -> str:
    return _html_to_md(path.read_text(encoding="utf-8", errors="ignore"))


def _from_url(url: str) -> str:
    import requests

    resp = requests.get(url, timeout=20, headers={"User-Agent": "open-toolkit-doc2md/0.1"})
    resp.raise_for_status()
    return _html_to_md(resp.text)


def convert(source: str) -> str:
    parsed = urlparse(source)
    if parsed.scheme in ("http", "https"):
        return _from_url(source)

    path = Path(source)
    if not path.exists():
        raise FileNotFoundError(f"not found: {source}")

    suffix = path.suffix.lower()
    if suffix == ".pdf":
        return _from_pdf(path)
    if suffix == ".docx":
        return _from_docx(path)
    if suffix in (".html", ".htm"):
        return _from_html_file(path)
    if suffix in (".txt", ".md"):
        return path.read_text(encoding="utf-8", errors="ignore")

    raise ValueError(f"unsupported file type: {suffix or '(none)'}")


def run(args) -> int:
    try:
        markdown = convert(args.source)
    except Exception as exc:  # noqa: BLE001 - CLI boundary, report and exit
        print(f"error: {exc}", file=sys.stderr)
        return 1

    if args.output:
        Path(args.output).write_text(markdown, encoding="utf-8")
        print(f"Wrote {args.output}")
    else:
        print(markdown)
    return 0


def add_subparser(subparsers):
    p = subparsers.add_parser(
        "doc2md",
        help="Convert a PDF, DOCX, HTML file, or URL into Markdown",
    )
    p.add_argument("source", help="Path to a .pdf/.docx/.html/.txt file, or a URL")
    p.add_argument("-o", "--output", help="Write output to a file instead of stdout")
    p.set_defaults(func=run)
