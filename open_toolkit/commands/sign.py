"""
toolkit sign — a tiny self-hosted e-signature tool. No server, no account,
no SaaS subscription: it stamps a text or image signature onto a PDF at
given coordinates, entirely on your own machine.
"""
from __future__ import annotations

import io
import sys
from pathlib import Path

from pypdf import PdfReader, PdfWriter
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas


def _page_sizes(reader: PdfReader):
    return [(p.mediabox.width, p.mediabox.height) for p in reader.pages]


def cmd_info(args) -> int:
    reader = PdfReader(args.pdf)
    print(f"{args.pdf}: {len(reader.pages)} page(s)")
    for i, (w, h) in enumerate(_page_sizes(reader)):
        print(f"  page {i + 1}: {float(w):.0f} x {float(h):.0f} pt")
    return 0


def cmd_apply(args) -> int:
    pdf_path = Path(args.pdf)
    reader = PdfReader(pdf_path)
    page_index = args.page - 1
    if page_index < 0 or page_index >= len(reader.pages):
        print(f"error: page {args.page} out of range (document has {len(reader.pages)} pages)", file=sys.stderr)
        return 1

    width = float(reader.pages[page_index].mediabox.width)
    height = float(reader.pages[page_index].mediabox.height)

    overlay_buf = io.BytesIO()
    c = canvas.Canvas(overlay_buf, pagesize=(width, height))

    if args.text:
        c.setFont(args.font, args.font_size)
        c.drawString(args.x, args.y, args.text)
    elif args.image:
        img = ImageReader(args.image)
        c.drawImage(
            img, args.x, args.y,
            width=args.image_width, height=args.image_height,
            mask="auto", preserveAspectRatio=True,
        )
    else:
        print("error: provide --text or --image for the signature", file=sys.stderr)
        return 1

    c.save()
    overlay_buf.seek(0)
    overlay_reader = PdfReader(overlay_buf)
    overlay_page = overlay_reader.pages[0]

    writer = PdfWriter()
    for i, page in enumerate(reader.pages):
        if i == page_index:
            page.merge_page(overlay_page)
        writer.add_page(page)

    out_path = Path(args.output) if args.output else pdf_path.with_stem(pdf_path.stem + "-signed")
    with open(out_path, "wb") as f:
        writer.write(f)
    print(f"Signed PDF written to {out_path}")
    return 0


def add_subparser(subparsers):
    p = subparsers.add_parser(
        "sign",
        help="Stamp a text or image signature onto a PDF (self-hosted, no account)",
    )
    sp = p.add_subparsers(dest="sign_command", required=True)

    info = sp.add_parser("info", help="Show page count and sizes, to help you pick coordinates")
    info.add_argument("pdf")
    info.set_defaults(func=cmd_info)

    apply_p = sp.add_parser("apply", help="Apply a signature to a page")
    apply_p.add_argument("pdf")
    apply_p.add_argument("--page", type=int, default=1, help="1-indexed page number (default: 1)")
    apply_p.add_argument("--x", type=float, required=True, help="X position in points, from bottom-left")
    apply_p.add_argument("--y", type=float, required=True, help="Y position in points, from bottom-left")
    apply_p.add_argument("--text", help="Draw this text as the signature")
    apply_p.add_argument("--font", default="Helvetica-Oblique", help="Font for --text (default: Helvetica-Oblique)")
    apply_p.add_argument("--font-size", type=float, default=18, help="Font size for --text (default: 18)")
    apply_p.add_argument("--image", help="Path to a signature image (PNG/JPG) instead of text")
    apply_p.add_argument("--image-width", type=float, default=150, help="Signature image width in points")
    apply_p.add_argument("--image-height", type=float, default=50, help="Signature image height in points")
    apply_p.add_argument("-o", "--output", help="Output path (default: <name>-signed.pdf)")
    apply_p.set_defaults(func=cmd_apply)
