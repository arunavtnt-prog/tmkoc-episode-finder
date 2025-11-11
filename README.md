# Business Plan PDF Generator

A professional business plan generation system featuring **Tufte-LaTeX** styling — the elegant, classic design used by Edward Tufte for his iconic books on data visualization and information design.

## Features

- **Tufte-LaTeX Design**: Beautiful typography with wide margins for sidenotes
- **Automated Chart Generation**: Professional financial visualizations from CSV data
- **PDF Rebranding**: Apply corporate identity to existing PDFs
- **Pandoc Integration**: Write in Markdown, output professional PDF
- **CI/CD Ready**: Automated builds with GitHub Actions

## Design Philosophy

This template uses Edward Tufte's design principles:

- **Wide margins** for sidenotes and margin figures
- **Elegant typography** (Palatino for body text, Helvetica for sans-serif)
- **Minimal, clean design** that prioritizes content
- **Tight integration** of text and graphics
- **Margin notes** for commentary and additional context

## Quick Start

### Prerequisites

**System Dependencies:**
- `pdflatex` - LaTeX PDF engine (from texlive-latex-extra)
- `python3` - For chart generation and PDF rebranding
- Tufte-LaTeX class files (included in repository)

**Installation:**

```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install texlive-latex-extra texlive-fonts-extra python3-pip

# macOS
brew install basictex python3
sudo tlmgr install tufte-latex changepage fancyhdr

# Python packages
make install
# or manually:
pip3 install pandas matplotlib PyPDF2 reportlab Pillow
```

### Generate Your Business Plan

```bash
# Generate everything (charts + PDF)
make all

# Or step by step:
make charts    # Generate financial charts
make pdf       # Build the Tufte-styled PDF
```

Output: `business-plan.pdf` (Tufte-LaTeX styled, ~192 KB)

## Project Structure

```
business-plan/
├── business-plan-tufte.tex          # Main Tufte-LaTeX document
├── tufte-book.cls                   # Tufte book class
├── tufte-common.def                 # Tufte common definitions
├── tufte-handout.cls                # Tufte handout class
├── data/
│   └── forecast.csv                 # Financial forecast data
├── scripts/
│   ├── generate_charts.py          # Generate charts from CSV
│   └── rebrand_pdf.py              # Rebrand existing PDFs
├── charts/                          # Generated charts (auto-created)
├── assets/                          # Images and logos (auto-created)
├── build.sh                         # Main build script
├── Makefile                         # Build automation
└── README.md                        # This file
```

## Customization

### Edit Content

The business plan is written directly in LaTeX using Tufte commands in `business-plan-tufte.tex`:

```latex
\chapter{Your Chapter}

\newthought{Start with emphasis} and continue your text.

\marginnote{
  Add notes in the margin
}

\sidenote{Or use sidenotes with numbers}

\begin{figure}
\includegraphics{your-chart.pdf}
\caption{Your figure caption}
\end{figure}
```

### Update Financial Data

Edit `data/forecast.csv` with your financial projections. Charts regenerate automatically on build.

### Tufte-Specific Features

**Margin Notes:**
```latex
\marginnote{Your note here}
```

**Sidenotes (numbered footnotes in margin):**
```latex
Some text\sidenote{Additional context}
```

**New Thought (section openings):**
```latex
\newthought{The first few words} of a new section
```

**Full-width Figures:**
```latex
\begin{figure*}
\includegraphics{wide-chart.pdf}
\caption{Spans across text and margin}
\end{figure*}
```

**Margin Tables:**
```latex
\begin{margintable}
\begin{tabular}{cc}
...
\end{tabular}
\caption{Table in margin}
\end{margintable}
```

**Full-width Tables:**
```latex
\begin{fullwidth}
\begin{table}
...
\end{table}
\end{fullwidth}
```

## Building the PDF

### Command Line

```bash
# Full Tufte compilation sequence
pdflatex business-plan-tufte.tex
pdflatex business-plan-tufte.tex
pdflatex business-plan-tufte.tex

# Or use the build script
./build.sh
```

### Make Targets

```bash
make all       # Generate charts and build PDF (default)
make charts    # Generate financial charts only
make pdf       # Build PDF with Tufte-LaTeX
make rebrand   # Create rebranded PDF example
make install   # Install Python dependencies
make clean     # Remove generated files
make help      # Show help message
```

## Charts

Three charts are automatically generated with modern gradient styling:

1. **Revenue Forecast** - Quarterly revenue with customer growth
2. **Expense Breakdown** - Revenue vs. expenses with profit line
3. **ARR Growth** - Annual recurring revenue trajectory

Charts are saved in both SVG (web) and PDF (LaTeX) formats and seamlessly integrate with the Tufte layout.

## PDF Rebranding

Transform existing PDFs with your corporate identity:

```bash
# Create example rebranded PDF
make rebrand

# Rebrand your own PDF
python3 scripts/rebrand_pdf.py input.pdf -o output.pdf \
    --company "Your Company" \
    --doc-type "Proposal" \
    --watermark
```

## CI/CD Integration

GitHub Actions workflow included (`.github/workflows/build.yml`):

```yaml
# Automatically builds PDF on push
# Uploads PDF as artifact
```

The workflow installs all required LaTeX packages and Python dependencies.

## Tufte-LaTeX Design Elements

### Typography
- **Body Text**: Palatino (beautiful serif for readability)
- **Headings**: Matching serif capitals
- **Sans-serif**: Helvetica (for contrast)
- **Line Spacing**: Generous, Tufte-calibrated

### Layout
- **Wide Margins**: ~1.5 inches for sidenotes and figures
- **Text Column**: Narrower for better readability
- **Margin Column**: For notes, small figures, tables
- **Full Width**: Available when needed

### Visual Integration
- Figures can be placed in margin or span full width
- Tables integrate naturally in text or margin
- Charts designed to complement text flow
- Minimal decoration, maximum clarity

## Troubleshooting

**"tufte-book.cls not found"**
- Ensure you've cloned the repository with all files
- Check that `tufte-book.cls` exists in project root

**"Package not found" errors**
- Install missing packages: `sudo tlmgr install <package-name>`
- Or install full texlive: `sudo apt-get install texlive-full`

**Charts not appearing**
- Run `make charts` first
- Verify `charts/*.pdf` files exist
- Check file paths in `.tex` file

**PDF has wrong margins**
- Tufte uses custom margins by design (this is normal)
- Wide right margin is for sidenotes and figures

## Design Inspiration

This template follows Edward Tufte's principles from:

- *The Visual Display of Quantitative Information*
- *Envisioning Information*
- *Beautiful Evidence*

Key principles:
- **Show the data** - let content speak
- **Induce the viewer to think** about substance
- **Make large data sets coherent**
- **Reveal data at several levels** of detail
- **Integrate** text, graphics, and data

## Examples

See generated examples:
- `business-plan.pdf` - Full Tufte-styled business plan (~192 KB)
- `example-rebranded.pdf` - Rebranded PDF with corporate styling

## File Sizes

- Tufte PDF: ~192 KB (24 pages)
- Charts: ~30-35 KB each (3 charts)
- Total package: Professional, elegant, readable

## Contributing

To extend this template:

1. **Add sections**: Follow Tufte commands in `.tex` file
2. **Add charts**: Edit `scripts/generate_charts.py`
3. **Customize styling**: Modify color definitions in `.tex`
4. **Add margin content**: Use `\marginnote` and `\sidenote`

## References

- [Tufte-LaTeX GitHub](https://github.com/Tufte-LaTeX/tufte-latex)
- [Edward Tufte's Website](https://www.edwardtufte.com)
- [Tufte-LaTeX Documentation](https://tufte-latex.github.io/tufte-latex/)

## License

This template is provided as-is for creating business documents. The Tufte-LaTeX classes are licensed under Apache License 2.0.

## Credits

- Design principles by [Edward Tufte](https://www.edwardtufte.com)
- Tufte-LaTeX by [Tufte-LaTeX developers](https://github.com/Tufte-LaTeX)
- Charts powered by [Matplotlib](https://matplotlib.org)
- Business plan template by Claude/Anthropic

---

**Need help?** Check the troubleshooting section or consult the Tufte-LaTeX documentation.

**Ready to build?** Run `make all` and generate your elegant, Tufte-styled business plan!
