#!/usr/bin/env python3
"""
Generate a complete PDF using mkdocs-pdf-export and split it into individual guides
"""

import os
import subprocess
import yaml
import re
from pathlib import Path
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from io import BytesIO

class PDFSplitter:
    def __init__(self):
        self.guides = [
            {
                'name': 'Overview Guide',
                'start_marker': 'Overview Guide',
                'end_marker': 'Senders Guide',
                'filename': 'studio3-overview-guide.pdf'
            },
            {
                'name': 'Senders Guide', 
                'start_marker': 'Senders Guide',
                'end_marker': 'Echoes Guide',
                'filename': 'studio3-senders-guide.pdf'
            },
            {
                'name': 'Echoes Guide',
                'start_marker': 'Echoes Guide', 
                'end_marker': 'Anchors Guide',
                'filename': 'studio3-echoes-guide.pdf'
            },
            {
                'name': 'Anchors Guide',
                'start_marker': 'Anchors Guide',
                'end_marker': None,  # Last guide
                'filename': 'studio3-anchors-guide.pdf'
            }
        ]
    
    def create_cover_page(self, guide_name):
        """Create a professional cover page for each guide"""
        packet = BytesIO()
        c = canvas.Canvas(packet, pagesize=A4)
        width, height = A4
        
        # Background gradient effect (simulated with rectangles)
        for i in range(100):
            gray = 250 - i * 0.5
            c.setFillColorRGB(gray/255, gray/255, gray/255)
            c.rect(0, height - i * height/100, width, height/100, fill=True, stroke=False)
        
        # Studio3 branding colors
        primary_color = HexColor('#2B4C8C')
        accent_color = HexColor('#E91E63')
        
        # Title
        c.setFillColor(primary_color)
        c.setFont("Helvetica-Bold", 48)
        title_y = height * 0.7
        c.drawCentredString(width/2, title_y, "Studio3")
        
        # Guide name
        c.setFillColor(accent_color)
        c.setFont("Helvetica-Bold", 36)
        c.drawCentredString(width/2, title_y - 80, guide_name)
        
        # Subtitle
        c.setFillColor(HexColor('#666666'))
        c.setFont("Helvetica", 18)
        c.drawCentredString(width/2, title_y - 130, "Complete Documentation")
        
        # Decorative line
        c.setStrokeColor(accent_color)
        c.setLineWidth(3)
        line_y = title_y - 160
        c.line(width*0.3, line_y, width*0.7, line_y)
        
        # Footer
        from datetime import datetime
        c.setFillColor(HexColor('#999999'))
        c.setFont("Helvetica", 12)
        c.drawCentredString(width/2, 60, f"Generated {datetime.now().strftime('%B %Y')}")
        
        c.save()
        packet.seek(0)
        return PdfReader(packet).pages[0]
    
    def find_guide_pages(self, pdf_reader, start_marker, end_marker=None):
        """Find the page range for a specific guide"""
        start_page = None
        end_page = None
        
        for i, page in enumerate(pdf_reader.pages):
            text = page.extract_text()
            
            # Look for start marker
            if start_page is None and start_marker in text:
                # Check if it's a section header (not just a mention)
                lines = text.split('\n')
                for line in lines[:10]:  # Check first 10 lines
                    if start_marker in line and len(line) < 100:  # Likely a header
                        start_page = i
                        break
            
            # Look for end marker
            if start_page is not None and end_marker and end_marker in text:
                lines = text.split('\n')
                for line in lines[:10]:
                    if end_marker in line and len(line) < 100:
                        end_page = i
                        break
                if end_page is not None:
                    break
        
        # If no end marker (last guide), use all remaining pages
        if start_page is not None and end_page is None:
            end_page = len(pdf_reader.pages)
        
        return start_page, end_page
    
    def split_pdf(self, input_path, output_dir):
        """Split the complete PDF into individual guide PDFs"""
        print(f"Reading {input_path}...")
        
        # Read the complete PDF
        with open(input_path, 'rb') as f:
            pdf_reader = PdfReader(f)
            total_pages = len(pdf_reader.pages)
            print(f"Total pages: {total_pages}")
            
            # Process each guide
            for guide in self.guides:
                print(f"\nProcessing {guide['name']}...")
                
                # Find page range
                start_page, end_page = self.find_guide_pages(
                    pdf_reader, 
                    guide['start_marker'], 
                    guide['end_marker']
                )
                
                if start_page is None:
                    print(f"  ⚠️  Could not find start of {guide['name']}")
                    continue
                
                print(f"  Pages: {start_page + 1} to {end_page}")
                
                # Create new PDF for this guide
                pdf_writer = PdfWriter()
                
                # Add cover page
                cover_page = self.create_cover_page(guide['name'])
                pdf_writer.add_page(cover_page)
                
                # Add guide pages
                for page_num in range(start_page, end_page):
                    pdf_writer.add_page(pdf_reader.pages[page_num])
                
                # Add metadata
                pdf_writer.add_metadata({
                    '/Title': f"Studio3 {guide['name']}",
                    '/Author': 'Studio3 Documentation',
                    '/Subject': 'Venture Building Platform Documentation',
                    '/Creator': 'MkDocs with Material theme'
                })
                
                # Write to file
                output_path = output_dir / guide['filename']
                with open(output_path, 'wb') as output_file:
                    pdf_writer.write(output_file)
                
                print(f"  ✓ Created {output_path.name}")
    
    def generate_complete_pdf(self):
        """Generate the complete PDF using mkdocs-pdf-export"""
        print("Generating complete PDF with mkdocs-pdf-export...")
        
        # Set environment variable to enable PDF export
        env = os.environ.copy()
        env['ENABLE_PDF_EXPORT'] = '1'
        
        # Build the site with PDF export
        result = subprocess.run(
            ['mkdocs', 'build', '--clean'],
            env=env,
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0:
            print("Error building site:")
            print(result.stderr)
            return None
        
        # Check if PDF was generated
        pdf_path = Path('site/pdf/studio3-complete-guide.pdf')
        if pdf_path.exists():
            size_mb = pdf_path.stat().st_size / (1024 * 1024)
            print(f"✓ Generated complete PDF: {size_mb:.1f} MB")
            return pdf_path
        else:
            print("✗ Complete PDF not found")
            return None

def main():
    """Main function"""
    splitter = PDFSplitter()
    
    # Create output directories
    site_pdf_dir = Path('site/pdf')
    site_pdf_dir.mkdir(parents=True, exist_ok=True)
    
    docs_pdf_dir = Path('docs/pdf')
    docs_pdf_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate complete PDF
    complete_pdf = splitter.generate_complete_pdf()
    
    if not complete_pdf:
        print("Failed to generate complete PDF")
        return
    
    # Split into individual guides
    print("\nSplitting PDF into individual guides...")
    splitter.split_pdf(complete_pdf, site_pdf_dir)
    
    # Copy to docs/pdf
    print("\nCopying to docs/pdf...")
    import shutil
    for guide in splitter.guides:
        src = site_pdf_dir / guide['filename']
        if src.exists():
            dst = docs_pdf_dir / guide['filename']
            shutil.copy2(src, dst)
            size_mb = dst.stat().st_size / (1024 * 1024)
            print(f"  ✓ {guide['filename']} ({size_mb:.1f} MB)")
    
    # Update index
    print("\nUpdating PDF index...")
    index_content = """# Studio3 Documentation PDFs

High-quality PDF versions of all Studio3 documentation guides.

## Available Guides

"""
    
    for guide in splitter.guides:
        pdf_path = docs_pdf_dir / guide['filename']
        if pdf_path.exists():
            size_mb = pdf_path.stat().st_size / (1024 * 1024)
            index_content += f"- [{guide['name']}]({guide['filename']}) - Complete guide with all sections ({size_mb:.1f} MB)\n"
    
    index_content += """

## Features

- Professional cover pages with Studio3 branding
- Complete content from all guide sections  
- Consistent formatting and typography
- Syntax-highlighted code blocks
- All original styles preserved
- Optimized for both printing and digital reading
- Bookmarks and navigation
- Searchable text

## Generation Method

These PDFs are generated using:
1. MkDocs with mkdocs-pdf-export plugin for complete styling
2. PyPDF2 for intelligent splitting into individual guides
3. ReportLab for professional cover pages

Last generated: """ + __import__('datetime').datetime.now().strftime('%B %d, %Y')
    
    with open(docs_pdf_dir / 'index.md', 'w') as f:
        f.write(index_content)
    
    print("\n✅ PDF generation complete!")

if __name__ == '__main__':
    # Check dependencies
    try:
        import PyPDF2
        import reportlab
    except ImportError:
        print("Installing required dependencies...")
        subprocess.run(['pip', 'install', 'PyPDF2', 'reportlab'], check=True)
    
    main()