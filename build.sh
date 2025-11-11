#!/bin/bash
# Build script for business plan PDF generation
# Requires: pandoc, xelatex, python3, matplotlib

set -e

echo "==================================="
echo "Business Plan PDF Builder"
echo "==================================="

# Configuration
INPUT_MD="plan.md"
OUTPUT_PDF="business-plan.pdf"
TUFTE_TEX="business-plan-tufte.tex"
TEMPLATE="templates/modern-template.tex"
CHARTS_DIR="charts"
ASSETS_DIR="assets"

# Check for required tools
check_dependencies() {
    local missing=()

    command -v pandoc >/dev/null 2>&1 || missing+=("pandoc")
    command -v xelatex >/dev/null 2>&1 || missing+=("texlive-xetex")
    command -v python3 >/dev/null 2>&1 || missing+=("python3")

    if [ ${#missing[@]} -ne 0 ]; then
        echo "Error: Missing required dependencies:"
        printf '  - %s\n' "${missing[@]}"
        echo ""
        echo "Install with:"
        echo "  Ubuntu/Debian: sudo apt-get install pandoc texlive-xetex texlive-fonts-extra python3 python3-pip"
        echo "  macOS: brew install pandoc basictex python3"
        echo "  Then: pip3 install pandas matplotlib pypdf2 reportlab"
        exit 1
    fi
}

# Create necessary directories
setup_directories() {
    echo "Setting up directories..."
    mkdir -p "$CHARTS_DIR" "$ASSETS_DIR"
}

# Create placeholder assets
create_assets() {
    echo "Creating placeholder assets..."

    # Create a simple logo using ImageMagick or Python
    if command -v convert >/dev/null 2>&1; then
        convert -size 300x100 xc:white \
                -font Arial -pointsize 36 -fill '#E86C38' \
                -gravity center -annotate +0+0 'AV' \
                "$ASSETS_DIR/logo.png" 2>/dev/null || true
    else
        # Fallback: create with Python if available
        python3 -c "
from PIL import Image, ImageDraw, ImageFont
img = Image.new('RGB', (300, 100), 'white')
d = ImageDraw.Draw(img)
d.text((150, 50), 'AV', fill='#E86C38', anchor='mm')
img.save('$ASSETS_DIR/logo.png')
        " 2>/dev/null || echo "  (Logo creation skipped - install ImageMagick or Pillow)"
    fi

    # Create placeholder cover background
    if [ ! -f "$ASSETS_DIR/cover-bg.png" ]; then
        touch "$ASSETS_DIR/cover-bg.png"
    fi
}

# Generate charts from data
generate_charts() {
    echo "Generating financial charts..."
    python3 scripts/generate_charts.py

    # Convert SVGs to PDF if needed
    if [ -f "scripts/fix_svgs.sh" ]; then
        bash scripts/fix_svgs.sh
    fi
}

# Build PDF with Tufte-LaTeX
build_pdf() {
    echo "Building PDF with Tufte-LaTeX..."

    # Use Tufte template (preferred)
    if [ -f "$TUFTE_TEX" ]; then
        echo "Using Tufte-LaTeX design system..."
        pdflatex -interaction=nonstopmode "$TUFTE_TEX" > /dev/null 2>&1
        pdflatex -interaction=nonstopmode "$TUFTE_TEX" > /dev/null 2>&1
        pdflatex -interaction=nonstopmode "$TUFTE_TEX" > /dev/null 2>&1

        if [ -f "business-plan-tufte.pdf" ]; then
            cp business-plan-tufte.pdf "$OUTPUT_PDF"
            local size=$(du -h "$OUTPUT_PDF" | cut -f1)
            echo "✓ PDF generated successfully: $OUTPUT_PDF ($size)"
        else
            echo "✗ Tufte PDF generation failed"
            exit 1
        fi
    else
        # Fallback to pandoc with modern template
        echo "Using modern template (Tufte not found)..."
        pandoc "$INPUT_MD" \
            --from markdown+yaml_metadata_block \
            --to pdf \
            --output "$OUTPUT_PDF" \
            --template="$TEMPLATE" \
            --pdf-engine=xelatex \
            --toc \
            --number-sections \
            2>&1 | grep -v "warning" || true

        if [ -f "$OUTPUT_PDF" ]; then
            local size=$(du -h "$OUTPUT_PDF" | cut -f1)
            echo "✓ PDF generated successfully: $OUTPUT_PDF ($size)"
        else
            echo "✗ PDF generation failed"
            exit 1
        fi
    fi
}

# Main execution
main() {
    check_dependencies
    setup_directories
    create_assets
    generate_charts
    build_pdf

    echo ""
    echo "==================================="
    echo "✓ Build complete!"
    echo "==================================="
    echo "Output: $OUTPUT_PDF"
    echo ""
}

# Run main function
main "$@"
