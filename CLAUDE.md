# CLAUDE.md - Project Context for Claude

## Project Overview
md2pdf is a Python CLI tool that converts Markdown files to PDF with customizable styling via YAML configuration. Uses xhtml2pdf for PDF rendering (pure Python, no system dependencies).

## Tech Stack
- Python 3.9+
- xhtml2pdf (PDF generation, pure Python)
- Click (CLI framework)
- Markdown (MD → HTML conversion)
- Jinja2 (header/footer template placeholders)
- PyYAML (config parsing)

## Architecture

```
CLI (cli.py) → Config (config.py) → Converter (converter.py) → Templates (templates.py)
```

1. CLI parses args, finds config file
2. Config loads YAML, merges with defaults
3. Converter reads MD, converts to HTML, calls templates
4. Templates generate full HTML document with embedded CSS
5. xhtml2pdf renders to PDF

## Key Files

| File | Purpose |
|------|---------|
| `src/md2pdf/cli.py` | Click-based CLI, entry point |
| `src/md2pdf/config.py` | Dataclasses for config, YAML loading, search hierarchy |
| `src/md2pdf/converter.py` | Core conversion: MD → HTML → PDF |
| `src/md2pdf/templates.py` | HTML document builder, CSS stylesheet generator |
| `pyproject.toml` | Dependencies, CLI entry point definition |

## Config Search Hierarchy
1. Same directory as input file: `md2pdf.yaml`
2. Current working directory: `md2pdf.yaml`
3. User home: `~/.md2pdf.yaml`

## Config Schema
```yaml
font:
  family: string    # CSS font-family
  size: string      # CSS font-size (e.g., "12pt")
  line_height: float

margins:
  top: string       # MUST be large enough for header (e.g., "4cm" for 2cm header)
  bottom: string    # MUST be large enough for footer
  left: string
  right: string

page_size: string   # "A4", "Letter", or "Legal"

header:
  height: string    # CSS length (e.g., "2cm")
  content: string   # HTML with Jinja2 placeholders

footer:
  height: string
  content: string
```

## Critical: Margin Configuration
**Top margin must be larger than header height** - the header is placed within the top margin area. Same applies to footer/bottom margin.

Example: For a 2cm header, set top margin to at least 3-4cm.

## Template Placeholders
- `{{title}}` - from first H1 or filename
- `{{filename}}` - input file name
- `{{date}}` - YYYY-MM-DD
- `{{datetime}}` - YYYY-MM-DD HH:MM
- `<span class="page-number"></span>` - converted to `<pdf:pagenumber>`
- `<span class="page-count"></span>` - converted to `<pdf:pagecount>`

## xhtml2pdf Specifics
- Uses `@page` CSS with `@frame` for header/footer areas
- Page numbers use special tags: `<pdf:pagenumber>`, `<pdf:pagecount>`
- Header/footer content placed in divs with IDs referenced by `-pdf-frame-content`
- **Use `<table>` for header/footer layouts** - flexbox doesn't work well
- Source divs hidden with `position: absolute; top: -1000pt`

## Coding Conventions
- Use type hints (Python 3.9+ syntax: `list[str]`, `dict[str, Any]`, `X | None`)
- Dataclasses for config structures
- Click decorators for CLI
- `from __future__ import annotations` at top of modules
- Keep functions focused and small
- Handle errors in CLI layer, not in library code

## Testing Changes
```bash
# Install in dev mode
pip install -e .

# Test basic conversion
md2pdf test.md -v

# Test with config
md2pdf test.md --config md2pdf.yaml

# Test flags
md2pdf test.md --no-config
md2pdf test.md -o output.pdf
```

## When Adding Features
1. **New config option**: Add to dataclass in `config.py`, update `merge_config()`, use in `templates.py`
2. **New placeholder**: Add to `extract_metadata()` in `converter.py`
3. **New CLI flag**: Add `@click.option()` in `cli.py`
4. **New styling**: Modify `generate_stylesheet()` in `templates.py`

## Important Patterns
- Config uses dataclasses with defaults - never None for optional config values
- xhtml2pdf uses `@frame` in `@page` rules for header/footer placement
- Page numbers converted from span placeholders to xhtml2pdf `<pdf:*>` tags in `_convert_page_placeholders()`
- Header/footer divs must be in document body for xhtml2pdf to find them
- Header/footer use table layouts, not flexbox (xhtml2pdf limitation)
