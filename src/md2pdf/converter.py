"""Core Markdown to PDF conversion logic."""

from __future__ import annotations

from datetime import datetime
from io import BytesIO
from pathlib import Path
from typing import Any

import markdown
from xhtml2pdf import pisa

from md2pdf.config import merge_config
from md2pdf.templates import build_html_document


def convert_markdown_to_pdf(
    input_file: Path,
    output_file: Path,
    user_config: dict[str, Any],
    verbose: bool = False,
) -> None:
    """Convert a Markdown file to PDF.

    Args:
        input_file: Path to the input Markdown file.
        output_file: Path to the output PDF file.
        user_config: User configuration dictionary.
        verbose: Enable verbose output.
    """
    # Merge configuration with defaults
    config = merge_config(user_config)

    # Read Markdown content
    markdown_content = input_file.read_text(encoding="utf-8")

    # Extract metadata for template placeholders
    metadata = extract_metadata(input_file, markdown_content)

    # Convert Markdown to HTML
    md = markdown.Markdown(output_format="html5")
    html_body = md.convert(markdown_content)

    # Build complete HTML document with embedded CSS
    html_document = build_html_document(
        body_content=html_body,
        config=config,
        metadata=metadata,
    )

    # Render PDF using xhtml2pdf
    with open(output_file, "wb") as pdf_file:
        pisa_status = pisa.CreatePDF(
            src=html_document,
            dest=pdf_file,
            encoding="utf-8",
        )

    if pisa_status.err:
        raise RuntimeError(f"PDF generation failed with {pisa_status.err} errors")


def extract_metadata(input_file: Path, content: str) -> dict[str, str]:
    """Extract metadata from file and content.

    Args:
        input_file: Path to the input file.
        content: File content.

    Returns:
        Dictionary of metadata values.
    """
    # Extract title from first H1 heading if present
    title = input_file.stem
    for line in content.split("\n"):
        line = line.strip()
        if line.startswith("# "):
            title = line[2:].strip()
            break

    return {
        "title": title,
        "filename": input_file.name,
        "date": datetime.now().strftime("%Y-%m-%d"),
        "datetime": datetime.now().strftime("%Y-%m-%d %H:%M"),
    }
