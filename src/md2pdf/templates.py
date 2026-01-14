"""HTML template generation for md2pdf."""

from __future__ import annotations

from jinja2 import Environment, BaseLoader

from md2pdf.config import Config


def build_html_document(
    body_content: str,
    config: Config,
    metadata: dict[str, str],
) -> str:
    """Build complete HTML document with embedded CSS for xhtml2pdf.

    Args:
        body_content: HTML content converted from Markdown.
        config: Configuration object.
        metadata: Document metadata for template placeholders.

    Returns:
        Complete HTML document string.
    """
    env = Environment(loader=BaseLoader())

    # Process header template - replace page number placeholders with xhtml2pdf tags
    header_html = ""
    if config.header.content:
        header_content = _convert_page_placeholders(config.header.content)
        header_template = env.from_string(header_content)
        header_html = header_template.render(**metadata)

    # Process footer template
    footer_html = ""
    if config.footer.content:
        footer_content = _convert_page_placeholders(config.footer.content)
        footer_template = env.from_string(footer_content)
        footer_html = footer_template.render(**metadata)

    # Generate stylesheet
    stylesheet = generate_stylesheet(config)

    # Build header/footer divs - these are pulled into frames by -pdf-frame-content
    header_div = f'<div id="header_div">{header_html}</div>' if header_html else ""
    footer_div = f'<div id="footer_div">{footer_html}</div>' if footer_html else ""

    # Build document
    document = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{metadata.get('title', 'Document')}</title>
    <style>
{stylesheet}
    </style>
</head>
<body>
    {header_div}
    {footer_div}
    {body_content}
</body>
</html>"""

    return document


def _convert_page_placeholders(content: str) -> str:
    """Convert CSS-style page placeholders to xhtml2pdf tags.

    Args:
        content: HTML content with placeholders.

    Returns:
        Content with xhtml2pdf-compatible page number tags.
    """
    # Replace span-based placeholders with xhtml2pdf PDF tags
    content = content.replace(
        '<span class="page-number"></span>',
        '<pdf:pagenumber>'
    )
    content = content.replace(
        '<span class="page-count"></span>',
        '<pdf:pagecount>'
    )
    return content


def generate_stylesheet(config: Config) -> str:
    """Generate CSS stylesheet for xhtml2pdf.

    Args:
        config: Configuration object.

    Returns:
        CSS stylesheet string.
    """
    css = f"""
@page {{
    size: {config.page_size};
    margin: {config.margins.top} {config.margins.right} {config.margins.bottom} {config.margins.left};

    @frame header {{
        -pdf-frame-content: header_div;
        top: 0.5cm;
        margin-left: {config.margins.left};
        margin-right: {config.margins.right};
        height: {config.header.height};
    }}

    @frame footer {{
        -pdf-frame-content: footer_div;
        bottom: 0.5cm;
        margin-left: {config.margins.left};
        margin-right: {config.margins.right};
        height: {config.footer.height};
    }}
}}

/* Hide the source divs - they get copied to frames */
#header_div {{
    position: absolute;
    top: -1000pt;
}}

#footer_div {{
    position: absolute;
    top: -1000pt;
}}

/* Base typography */
body {{
    font-family: {config.font.family};
    font-size: {config.font.size};
    line-height: {config.font.line_height};
    color: #1a1a1a;
}}

/* Headings */
h1, h2, h3, h4, h5, h6 {{
    margin-top: 1.2em;
    margin-bottom: 0.5em;
    line-height: 1.3;
}}

h1 {{ font-size: 1.8em; }}
h2 {{ font-size: 1.4em; }}
h3 {{ font-size: 1.2em; }}
h4 {{ font-size: 1.1em; }}
h5, h6 {{ font-size: 1em; }}

h1:first-child, h2:first-child, h3:first-child {{
    margin-top: 0;
}}

/* Paragraphs */
p {{
    margin-top: 0;
    margin-bottom: 0.8em;
}}

/* Code blocks */
pre {{
    background-color: #f5f5f5;
    padding: 0.8em;
    font-family: "Courier New", Courier, monospace;
    font-size: 0.85em;
    white-space: pre-wrap;
    word-wrap: break-word;
}}

code {{
    font-family: "Courier New", Courier, monospace;
    font-size: 0.9em;
    background-color: #f5f5f5;
    padding: 0.1em 0.3em;
}}

pre code {{
    background: none;
    padding: 0;
}}

/* Blockquotes */
blockquote {{
    margin: 1em 0;
    padding-left: 1em;
    border-left: 3px solid #ddd;
    color: #666;
}}

/* Lists */
ul, ol {{
    margin: 0.8em 0;
    padding-left: 1.5em;
}}

li {{
    margin-bottom: 0.2em;
}}

/* Links */
a {{
    color: #0066cc;
    text-decoration: none;
}}

/* Images */
img {{
    max-width: 100%;
    height: auto;
}}

/* Tables */
table {{
    width: 100%;
    border-collapse: collapse;
    margin: 1em 0;
}}

th, td {{
    padding: 0.4em;
    text-align: left;
    border-bottom: 1px solid #ddd;
}}

th {{
    font-weight: bold;
    background-color: #f5f5f5;
}}

/* Horizontal rules */
hr {{
    border: none;
    border-top: 1px solid #ddd;
    margin: 1.5em 0;
}}
"""

    return css
