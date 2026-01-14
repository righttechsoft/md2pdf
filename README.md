# md2pdf

Convert Markdown files to PDF with customizable styling.

## Installation

```bash
pip install -e .
```

No external dependencies required - works on Windows, macOS, and Linux.

## Usage

```bash
# Basic conversion
md2pdf document.md

# Specify output file
md2pdf document.md -o output.pdf

# Use specific config file
md2pdf document.md --config my-config.yaml

# Verbose output
md2pdf document.md -v

# Ignore config files, use defaults
md2pdf document.md --no-config
```

## Configuration

Create a `md2pdf.yaml` file to customize styling. The tool searches for config in:
1. Same directory as the input file
2. Current working directory
3. Home directory (`~/.md2pdf.yaml`)

### Example Configuration

```yaml
# Font settings
font:
  family: "Georgia, serif"
  size: "12pt"
  line_height: 1.6

# Page margins - IMPORTANT: top margin must be large enough for header
margins:
  top: "4cm"      # Increase if using header
  bottom: "2.5cm" # Increase if using footer
  left: "2cm"
  right: "2cm"

# Page size: A4, Letter, Legal
page_size: "A4"

# Header (appears on every page)
header:
  height: "2cm"
  content: |
    <table style="width: 100%; border: none;">
      <tr>
        <td style="text-align: left; border: none;"><img src="logo.png" style="height: 1.2cm;" /></td>
        <td style="text-align: center; font-size: 10pt; color: #666; border: none;">{{title}}</td>
        <td style="text-align: right; font-size: 9pt; color: #888; border: none;">{{date}}</td>
      </tr>
    </table>

# Footer (appears on every page)
footer:
  height: "1.5cm"
  content: |
    <table style="width: 100%; border: none;">
      <tr>
        <td style="text-align: left; font-size: 8pt; color: #999; border: none;">{{filename}}</td>
        <td style="text-align: center; font-size: 9pt; color: #666; border: none;">Page <span class="page-number"></span> of <span class="page-count"></span></td>
        <td style="text-align: right; border: none;"><img src="logo.png" style="height: 0.8cm;" /></td>
      </tr>
    </table>
```

### Important Notes

- **Margins must accommodate header/footer**: If using a 2cm header, set top margin to at least 3-4cm
- **Use tables for layout**: xhtml2pdf works best with `<table>` layouts instead of CSS flexbox
- **Images**: Place image files in the same directory as the markdown file

### Available Placeholders

| Placeholder | Description |
|-------------|-------------|
| `{{title}}` | Document title (from first H1 or filename) |
| `{{filename}}` | Input filename |
| `{{date}}` | Current date (YYYY-MM-DD) |
| `{{datetime}}` | Current date and time |
| `<span class="page-number"></span>` | Current page number |
| `<span class="page-count"></span>` | Total page count |

## License

MIT License - see LICENSE file.
