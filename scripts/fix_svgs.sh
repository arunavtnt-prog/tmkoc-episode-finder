#!/bin/bash
# Convert SVG charts to PDF format for LaTeX inclusion
# Uses Inkscape or Cairo for high-quality conversion

set -e

CHARTS_DIR="charts"

echo "Converting SVG charts to PDF..."

# Check for available conversion tools
if command -v inkscape &> /dev/null; then
    CONVERTER="inkscape"
    echo "Using Inkscape for conversion"
elif command -v cairosvg &> /dev/null; then
    CONVERTER="cairosvg"
    echo "Using CairoSVG for conversion"
elif command -v rsvg-convert &> /dev/null; then
    CONVERTER="rsvg"
    echo "Using rsvg-convert for conversion"
else
    echo "Warning: No SVG converter found (inkscape, cairosvg, or rsvg-convert)"
    echo "SVG to PDF conversion skipped - using existing PDFs"
    exit 0
fi

# Convert each SVG to PDF
for svg_file in "$CHARTS_DIR"/*.svg; do
    if [ -f "$svg_file" ]; then
        pdf_file="${svg_file%.svg}.pdf"
        echo "  Converting $(basename "$svg_file") -> $(basename "$pdf_file")"

        case $CONVERTER in
            inkscape)
                inkscape "$svg_file" --export-filename="$pdf_file" --export-area-drawing 2>/dev/null
                ;;
            cairosvg)
                cairosvg "$svg_file" -o "$pdf_file"
                ;;
            rsvg)
                rsvg-convert -f pdf -o "$pdf_file" "$svg_file"
                ;;
        esac
    fi
done

echo "✓ SVG to PDF conversion complete"
