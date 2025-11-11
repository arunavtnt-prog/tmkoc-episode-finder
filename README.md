# Business Plan PDF Generator

A professional, automated business plan generation system with beautiful LaTeX styling inspired by Anthropic's design aesthetic. Generate stunning business plan PDFs complete with financial charts and the ability to rebrand existing PDFs.

## Features

- **Beautiful LaTeX Template**: Clean, modern design inspired by Anthropic's branding
- **Automated Chart Generation**: Creates professional financial visualizations from CSV data
- **PDF Rebranding**: Take any existing PDF and apply your corporate identity
- **Pandoc Integration**: Write in Markdown, output professional PDF
- **CI/CD Ready**: Automated builds with GitHub Actions
- **Fully Customizable**: Easy to modify colors, fonts, and layouts

## Quick Start

### Prerequisites

**System Dependencies:**
- `pandoc` - Document converter
- `xelatex` - LaTeX PDF engine (from texlive)
- `python3` - For chart generation and PDF rebranding

**Installation:**

```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install pandoc texlive-xetex texlive-fonts-extra python3 python3-pip

# macOS
brew install pandoc basictex python3

# Python packages
make install
# or manually:
pip3 install pandas matplotlib PyPDF2 reportlab
```

### Generate Your Business Plan

```bash
# Generate everything (charts + PDF)
make all

# Or step by step:
make charts    # Generate financial charts
make pdf       # Build the PDF
```

Output: `business-plan.pdf`

## Project Structure

```
business-plan/
├── plan.md                          # Main business plan content (Markdown + YAML)
├── templates/
│   └── corporate-template.tex       # LaTeX template (Anthropic-inspired design)
├── data/
│   └── forecast.csv                 # Financial forecast data
├── scripts/
│   ├── generate_charts.py          # Generate charts from CSV
│   ├── fix_svgs.sh                 # Convert SVGs to PDF
│   └── rebrand_pdf.py              # Rebrand existing PDFs
├── charts/                          # Generated charts (auto-created)
├── assets/                          # Images and logos (auto-created)
├── build.sh                         # Main build script
├── Makefile                         # Build automation
└── README.md                        # This file
```

## Customization

### Edit Content

Edit `plan.md` to customize your business plan content. Uses YAML frontmatter for metadata:

```yaml
---
title: "Your Company Name"
subtitle: "Business Plan 2025-2027"
author: "Your Name"
date: "March 2025"
---

# Your Content Here
```

### Update Financial Data

Edit `data/forecast.csv` with your financial projections:

```csv
Quarter,Year,Revenue,Expenses,Customers,ARR
Q1,2025,150000,450000,15,600000
Q2,2025,350000,520000,35,1400000
...
```

Charts are automatically regenerated on build.

### Customize Design

**Colors:** Edit `templates/corporate-template.tex`

```latex
\definecolor{anthropicOrange}{RGB}{232, 108, 56}
\definecolor{anthroBlack}{RGB}{25, 25, 25}
```

**Fonts:** The template uses Inter font (falls back to Arial)

```latex
\setmainfont{Inter}
```

To use custom fonts:
1. Place font files in `fonts/` directory
2. Update `\setmainfont` in template

**Chart Colors:** Edit `scripts/generate_charts.py`

```python
COLORS = {
    'orange': '#E86C38',
    'dark_orange': '#BF4C21',
    ...
}
```

## PDF Rebranding

Transform existing PDFs with your corporate identity:

```bash
# Create example rebranded PDF
make rebrand

# Rebrand your own PDF
python3 scripts/rebrand_pdf.py input.pdf -o output.pdf \
    --company "Your Company" \
    --doc-type "Proposal" \
    --watermark \
    --watermark-text "CONFIDENTIAL"
```

**Options:**
- `--company`: Company name for header
- `--doc-type`: Document type label
- `--watermark`: Enable watermark overlay
- `--watermark-text`: Watermark text (default: DRAFT)
- `--no-header`: Disable header
- `--no-footer`: Disable footer
- `--no-accent`: Disable accent bar

## Charts

Three charts are automatically generated:

1. **Revenue Forecast** - Quarterly revenue with customer growth
2. **Expense Breakdown** - Revenue vs. expenses with profit line
3. **ARR Growth** - Annual recurring revenue trajectory

Charts are saved in both SVG (web) and PDF (LaTeX) formats.

## CI/CD Integration

GitHub Actions workflow included (`.github/workflows/build.yml`):

```yaml
# Automatically builds PDF on push
# Uploads PDF as artifact
# Can be extended for automatic releases
```

## Make Targets

```bash
make all       # Generate charts and build PDF (default)
make charts    # Generate financial charts only
make pdf       # Build PDF from markdown
make rebrand   # Create rebranded PDF example
make install   # Install Python dependencies
make clean     # Remove generated files
make help      # Show help message
```

## Troubleshooting

**"pandoc: command not found"**
- Install pandoc: `sudo apt-get install pandoc` or `brew install pandoc`

**"xelatex: command not found"**
- Install texlive: `sudo apt-get install texlive-xetex texlive-fonts-extra`

**"No module named 'pandas'"**
- Install Python packages: `make install` or `pip3 install pandas matplotlib`

**LaTeX errors about missing fonts**
- The template falls back to Arial if Inter is not available
- Install Inter font from https://rsms.me/inter/ or use system fonts

**Charts not appearing in PDF**
- Ensure charts are generated: `make charts`
- Check that `charts/*.pdf` files exist
- Verify file paths in `plan.md` match generated chart names

## Design Philosophy

This template follows Anthropic's design principles:

- **Clean & Minimal**: Focus on content, not decoration
- **Professional**: Suitable for investor presentations and business use
- **Accessible**: High contrast, readable fonts, clear hierarchy
- **Modern**: Contemporary design that feels fresh and innovative

**Color Palette:**
- Primary: Warm orange (#E86C38) - energy and innovation
- Accent: Dark orange (#BF4C21) - depth and sophistication
- Text: Near-black (#191919) - readability
- Secondary: Professional blue (#2D6DA4) - trust

## Examples

See generated examples:
- `business-plan.pdf` - Full business plan with charts
- `example-rebranded.pdf` - Rebranded PDF with corporate styling

## Contributing

To extend this template:

1. **Add new chart types**: Edit `scripts/generate_charts.py`
2. **Customize template**: Modify `templates/corporate-template.tex`
3. **Enhance rebranding**: Extend `scripts/rebrand_pdf.py`
4. **Add sections**: Edit `plan.md` structure

## License

This template is provided as-is for creating business documents. Customize freely for your needs.

## Credits

- Design inspired by [Anthropic](https://www.anthropic.com)'s visual identity
- Built with [Pandoc](https://pandoc.org), [XeLaTeX](https://www.latex-project.org), and [Python](https://www.python.org)
- Charts powered by [Matplotlib](https://matplotlib.org)

---

**Need help?** Check the troubleshooting section or open an issue.

**Ready to build?** Run `make all` and generate your professional business plan!
