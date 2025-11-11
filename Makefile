# Makefile for Business Plan PDF Generation
#
# Targets:
#   make all       - Generate charts and build PDF (default)
#   make charts    - Generate financial charts only
#   make pdf       - Build PDF from markdown (assumes charts exist)
#   make rebrand   - Create rebranded PDF example
#   make clean     - Remove generated files
#   make install   - Install Python dependencies

.PHONY: all charts pdf rebrand clean install help

# Default target
all: charts pdf

# Generate financial charts from CSV data
charts:
	@echo "Generating charts..."
	@python3 scripts/generate_charts.py
	@bash scripts/fix_svgs.sh 2>/dev/null || true

# Build PDF from markdown using pandoc
pdf:
	@echo "Building PDF..."
	@bash build.sh

# Create rebranded PDF example
rebrand: example-input.pdf
	@echo "Creating rebranded PDF..."
	@python3 scripts/rebrand_pdf.py example-input.pdf -o example-rebranded.pdf \
		--company "Anthropic Ventures" \
		--doc-type "Business Plan" \
		--watermark \
		--watermark-text "CONFIDENTIAL"
	@echo "✓ Rebranded PDF created: example-rebranded.pdf"

# Create sample input PDF for rebranding demo
example-input.pdf:
	@echo "Creating sample PDF..."
	@python3 scripts/rebrand_pdf.py --create-sample

# Install Python dependencies
install:
	@echo "Installing Python dependencies..."
	@pip3 install pandas matplotlib PyPDF2 reportlab
	@echo "✓ Dependencies installed"
	@echo ""
	@echo "Note: You also need pandoc and xelatex installed:"
	@echo "  Ubuntu/Debian: sudo apt-get install pandoc texlive-xetex texlive-fonts-extra"
	@echo "  macOS: brew install pandoc basictex"

# Clean generated files
clean:
	@echo "Cleaning generated files..."
	@rm -f business-plan.pdf
	@rm -f example-input.pdf example-rebranded.pdf
	@rm -rf charts/*.svg charts/*.pdf
	@rm -rf assets/*.png
	@echo "✓ Clean complete"

# Help target
help:
	@echo "Business Plan PDF Generator"
	@echo ""
	@echo "Available targets:"
	@echo "  make all       - Generate charts and build PDF (default)"
	@echo "  make charts    - Generate financial charts from data/forecast.csv"
	@echo "  make pdf       - Build PDF from plan.md using pandoc + LaTeX"
	@echo "  make rebrand   - Create example of rebranded PDF"
	@echo "  make install   - Install Python dependencies"
	@echo "  make clean     - Remove all generated files"
	@echo "  make help      - Show this help message"
	@echo ""
	@echo "Prerequisites:"
	@echo "  - pandoc, xelatex (texlive)"
	@echo "  - Python 3 with pandas, matplotlib, PyPDF2, reportlab"
	@echo ""
	@echo "Quick start:"
	@echo "  make install   # Install dependencies"
	@echo "  make all       # Generate everything"
