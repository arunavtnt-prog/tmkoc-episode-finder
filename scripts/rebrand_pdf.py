#!/usr/bin/env python3
"""
PDF Rebranding Tool
Takes an existing PDF and rebrands it with new styling, header, footer, and watermark.
Extracts content and applies new corporate template.
"""

import sys
import argparse
from pathlib import Path
from io import BytesIO
import subprocess
import tempfile

try:
    from PyPDF2 import PdfReader, PdfWriter, Transformation
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.units import inch
    from reportlab.lib.colors import HexColor
except ImportError:
    print("Error: Required packages not found.")
    print("Install with: pip install PyPDF2 reportlab")
    sys.exit(1)

# Anthropic-inspired colors
ORANGE = HexColor('#E86C38')
DARK_ORANGE = HexColor('#BF4C21')
BLACK = HexColor('#191919')
GRAY = HexColor('#5F5F5F')
LIGHT_GRAY = HexColor('#F5F5F5')

def create_overlay(page_num, total_pages, branding_config):
    """Create a branded overlay for a PDF page."""
    packet = BytesIO()
    can = canvas.Canvas(packet, pagesize=letter)
    width, height = letter

    # Header
    if branding_config.get('header', True):
        can.setFillColor(ORANGE)
        can.rect(0, height - 0.5*inch, width, 0.5*inch, fill=True, stroke=False)

        can.setFillColor(BLACK)
        can.setFont("Helvetica-Bold", 14)
        can.drawString(0.5*inch, height - 0.35*inch, branding_config.get('company', 'Your Company'))

        can.setFillColor(GRAY)
        can.setFont("Helvetica", 10)
        can.drawRightString(width - 0.5*inch, height - 0.35*inch,
                           branding_config.get('document_type', 'Business Document'))

    # Footer
    if branding_config.get('footer', True):
        can.setFillColor(LIGHT_GRAY)
        can.rect(0, 0, width, 0.4*inch, fill=True, stroke=False)

        can.setFillColor(GRAY)
        can.setFont("Helvetica", 9)
        can.drawString(0.5*inch, 0.15*inch, f"© 2025 {branding_config.get('company', 'Your Company')}")
        can.drawCentredString(width/2, 0.15*inch, f"Page {page_num} of {total_pages}")
        can.drawRightString(width - 0.5*inch, 0.15*inch, "Confidential")

    # Watermark (if enabled)
    if branding_config.get('watermark', False):
        can.saveState()
        can.translate(width/2, height/2)
        can.rotate(45)
        can.setFillColor(ORANGE)
        can.setFont("Helvetica-Bold", 60)
        can.setFillAlpha(0.1)
        can.drawCentredString(0, 0, branding_config.get('watermark_text', 'DRAFT'))
        can.restoreState()

    # Left accent bar
    if branding_config.get('accent_bar', True):
        can.setFillColor(ORANGE)
        can.rect(0, 0.5*inch, 0.15*inch, height - inch, fill=True, stroke=False)

    can.save()
    packet.seek(0)
    return packet

def rebrand_pdf(input_path, output_path, branding_config):
    """Rebrand an existing PDF with new styling."""
    print(f"Rebranding PDF: {input_path}")

    # Read input PDF
    reader = PdfReader(input_path)
    writer = PdfWriter()
    total_pages = len(reader.pages)

    print(f"Processing {total_pages} pages...")

    for page_num, page in enumerate(reader.pages, start=1):
        # Create overlay for this page
        overlay_packet = create_overlay(page_num, total_pages, branding_config)
        overlay_reader = PdfReader(overlay_packet)
        overlay_page = overlay_reader.pages[0]

        # Merge original page with overlay
        page.merge_page(overlay_page)
        writer.add_page(page)

        if page_num % 10 == 0:
            print(f"  Processed {page_num}/{total_pages} pages")

    # Add metadata
    writer.add_metadata({
        '/Title': branding_config.get('title', 'Rebranded Document'),
        '/Author': branding_config.get('company', 'Your Company'),
        '/Subject': branding_config.get('subject', 'Business Document'),
        '/Creator': 'PDF Rebranding Tool',
        '/Producer': 'PyPDF2 + ReportLab'
    })

    # Write output
    with open(output_path, 'wb') as output_file:
        writer.write(output_file)

    print(f"✓ Rebranded PDF saved to: {output_path}")

def create_sample_pdf(output_path):
    """Create a sample PDF for demonstration."""
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak

    doc = SimpleDocTemplate(str(output_path), pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    # Title
    title = Paragraph("Sample Business Proposal", styles['Title'])
    story.append(title)
    story.append(Spacer(1, 0.3*inch))

    # Content
    content = [
        ("Executive Summary", """
        This is a sample business proposal document that demonstrates the PDF rebranding
        capability. In a real scenario, you would use your existing PDF documents and
        rebrand them with your corporate identity.
        """),
        ("Our Solution", """
        Our platform provides cutting-edge solutions for modern businesses. We combine
        innovative technology with deep industry expertise to deliver exceptional value.
        Key benefits include automated workflows, real-time analytics, and seamless
        integration with existing systems.
        """),
        ("Implementation Approach", """
        We follow a structured implementation methodology that ensures smooth deployment
        and rapid time-to-value. Our approach includes discovery, design, development,
        testing, and deployment phases, with ongoing support and optimization.
        """),
        ("Investment & ROI", """
        The proposed investment is $500,000 over 12 months, with expected ROI of 250%
        within 24 months. Cost savings from automation and efficiency gains will offset
        the initial investment within the first year of operation.
        """),
    ]

    for heading, text in content:
        story.append(Paragraph(heading, styles['Heading2']))
        story.append(Spacer(1, 0.1*inch))
        story.append(Paragraph(text, styles['BodyText']))
        story.append(Spacer(1, 0.2*inch))

    # Second page
    story.append(PageBreak())

    story.append(Paragraph("Financial Projections", styles['Heading2']))
    story.append(Spacer(1, 0.1*inch))
    story.append(Paragraph("""
    Year 1: $2.5M revenue, 50 customers, breakeven achieved in Q4<br/>
    Year 2: $12M revenue, 200 customers, 35% profit margin<br/>
    Year 3: $45M revenue, 600 customers, 45% profit margin<br/><br/>

    Our financial model is based on conservative assumptions and validated through
    extensive market research. We have strong unit economics with a 6:1 LTV:CAC ratio
    and 8-month payback period.
    """, styles['BodyText']))

    story.append(Spacer(1, 0.3*inch))
    story.append(Paragraph("Conclusion", styles['Heading2']))
    story.append(Spacer(1, 0.1*inch))
    story.append(Paragraph("""
    This proposal represents a unique opportunity to invest in a high-growth technology
    company with proven product-market fit and a clear path to market leadership. We
    look forward to discussing this opportunity with you in detail.
    """, styles['BodyText']))

    doc.build(story)
    print(f"✓ Created sample PDF: {output_path}")

def main():
    parser = argparse.ArgumentParser(
        description='Rebrand existing PDFs with new corporate styling'
    )
    parser.add_argument('input', nargs='?', help='Input PDF file to rebrand')
    parser.add_argument('-o', '--output', help='Output PDF file (default: input_rebranded.pdf)')
    parser.add_argument('--company', default='Anthropic Ventures', help='Company name')
    parser.add_argument('--doc-type', default='Business Plan', help='Document type')
    parser.add_argument('--watermark', action='store_true', help='Add watermark')
    parser.add_argument('--watermark-text', default='DRAFT', help='Watermark text')
    parser.add_argument('--no-header', action='store_true', help='Disable header')
    parser.add_argument('--no-footer', action='store_true', help='Disable footer')
    parser.add_argument('--no-accent', action='store_true', help='Disable accent bar')
    parser.add_argument('--create-sample', action='store_true',
                       help='Create sample PDF for demonstration')

    args = parser.parse_args()

    # Create sample if requested
    if args.create_sample:
        sample_path = Path('example-input.pdf')
        create_sample_pdf(sample_path)
        if not args.input:
            print(f"\nTo rebrand this sample, run:")
            print(f"  python {sys.argv[0]} example-input.pdf -o example-rebranded.pdf")
            return
        args.input = str(sample_path)

    if not args.input:
        parser.print_help()
        return

    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: Input file not found: {input_path}")
        sys.exit(1)

    # Determine output path
    if args.output:
        output_path = Path(args.output)
    else:
        output_path = input_path.parent / f"{input_path.stem}_rebranded.pdf"

    # Branding configuration
    branding_config = {
        'company': args.company,
        'document_type': args.doc_type,
        'watermark': args.watermark,
        'watermark_text': args.watermark_text,
        'header': not args.no_header,
        'footer': not args.no_footer,
        'accent_bar': not args.no_accent,
        'title': f'{args.doc_type} - {args.company}'
    }

    # Rebrand the PDF
    rebrand_pdf(input_path, output_path, branding_config)

if __name__ == '__main__':
    main()
