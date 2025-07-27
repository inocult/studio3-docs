#!/usr/bin/env python3
"""
Generate a single comprehensive PDF and split it into individual guides
"""

import os
import subprocess
import time
from pathlib import Path
from PyPDF2 import PdfReader, PdfWriter
import re

class PDFGenerator:
    def __init__(self):
        self.guides = [
            {
                'name': 'Overview Guide',
                'start_patterns': [
                    'Overview Guide',
                    'Understanding Studio3',
                    'What is Studio3?'
                ],
                'end_patterns': [
                    'Senders Guide',
                    'Build in Public'
                ],
                'filename': 'studio3-overview-guide.pdf'
            },
            {
                'name': 'Senders Guide',
                'start_patterns': [
                    'Senders Guide',
                    'Build in Public',
                    'Founder\'s handbook'
                ],
                'end_patterns': [
                    'Echoes Guide',
                    'Signal Your Conviction'
                ],
                'filename': 'studio3-senders-guide.pdf'
            },
            {
                'name': 'Echoes Guide',
                'start_patterns': [
                    'Echoes Guide',
                    'Signal Your Conviction',
                    'Master the art of belief'
                ],
                'end_patterns': [
                    'Anchors Guide',
                    'Guide the Ecosystem'
                ],
                'filename': 'studio3-echoes-guide.pdf'
            },
            {
                'name': 'Anchors Guide',
                'start_patterns': [
                    'Anchors Guide',
                    'Guide the Ecosystem',
                    'The complete handbook for validators'
                ],
                'end_patterns': None,  # Last guide
                'filename': 'studio3-anchors-guide.pdf'
            }
        ]
    
    def generate_complete_pdf(self):
        """Generate a single comprehensive PDF containing all guides"""
        print("Step 1: Generating complete PDF with all guides...")
        
        # Set environment variable to enable PDF export
        env = os.environ.copy()
        env['ENABLE_PDF_EXPORT'] = '1'
        
        # Clean previous builds
        if Path('site').exists():
            subprocess.run(['rm', '-rf', 'site'], check=True)
        
        print("  Building site with PDF export enabled...")
        
        # Build with PDF export
        result = subprocess.run(
            ['mkdocs', 'build', '--clean', '--verbose'],
            env=env,
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0:
            print("  ✗ Error building site:")
            print(result.stderr)
            # Try without verbose flag
            result = subprocess.run(
                ['mkdocs', 'build', '--clean'],
                env=env,
                capture_output=True,
                text=True
            )
            
            if result.returncode != 0:
                return None
        
        # Look for the generated PDF
        pdf_path = Path('site/pdf/studio3-complete-guide.pdf')
        
        if not pdf_path.exists():
            # Try to find any PDF that was generated
            pdf_files = list(Path('site').rglob('*.pdf'))
            if pdf_files:
                print(f"  Found PDF at: {pdf_files[0]}")
                pdf_path = pdf_files[0]
            else:
                print("  ✗ No PDF found. Trying alternative generation...")
                return self.generate_with_print_pdf()
        
        size_mb = pdf_path.stat().st_size / (1024 * 1024)
        print(f"  ✓ Generated complete PDF: {pdf_path} ({size_mb:.1f} MB)")
        return pdf_path
    
    def generate_with_print_pdf(self):
        """Alternative: Generate PDF by serving the site and using print functionality"""
        print("\n  Trying alternative PDF generation method...")
        
        # Start the server
        print("  Starting MkDocs server...")
        server = subprocess.Popen(
            ['mkdocs', 'serve', '--no-livereload'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        # Wait for server to start
        time.sleep(5)
        
        try:
            # Create a simple HTML that loads all content
            html_content = """
<!DOCTYPE html>
<html>
<head>
    <title>Studio3 Complete Documentation</title>
    <style>
        @media print {
            .pagebreak { page-break-before: always; }
        }
    </style>
</head>
<body>
    <h1>Loading Studio3 Documentation...</h1>
    <p>Please use your browser's print function to save as PDF.</p>
    <p>Make sure to:</p>
    <ul>
        <li>Enable background graphics</li>
        <li>Set margins to "Default"</li>
        <li>Save as PDF</li>
    </ul>
    
    <div class="pagebreak"></div>
    
    <iframe src="http://localhost:8000/" width="100%" height="1000px"></iframe>
</body>
</html>
"""
            
            temp_html = Path('temp_complete.html')
            with open(temp_html, 'w') as f:
                f.write(html_content)
            
            print(f"  ✓ Created temporary HTML: {temp_html}")
            print("  ⚠️  Please open this file in a browser and print to PDF")
            
            return None
            
        finally:
            # Stop server
            server.terminate()
            server.wait()
    
    def find_page_ranges(self, pdf_reader):
        """Find the page ranges for each guide in the complete PDF"""
        page_ranges = {}
        total_pages = len(pdf_reader.pages)
        
        print(f"\nStep 2: Analyzing PDF structure ({total_pages} pages)...")
        
        for guide_idx, guide in enumerate(self.guides):
            print(f"\n  Looking for {guide['name']}...")
            
            start_page = None
            end_page = None
            
            # Search for start page
            for page_num in range(total_pages):
                if start_page is not None and end_page is not None:
                    break
                
                page = pdf_reader.pages[page_num]
                text = page.extract_text()
                
                # Clean text for better matching
                text_lines = text.split('\n')
                
                # Look for start patterns
                if start_page is None:
                    for line in text_lines[:20]:  # Check first 20 lines
                        line_clean = line.strip()
                        for pattern in guide['start_patterns']:
                            if pattern.lower() in line_clean.lower() and len(line_clean) < 100:
                                print(f"    Found start at page {page_num + 1}: '{line_clean}'")
                                start_page = page_num
                                break
                        if start_page is not None:
                            break
                
                # Look for end patterns
                if start_page is not None and end_page is None and guide['end_patterns']:
                    for line in text_lines[:20]:
                        line_clean = line.strip()
                        for pattern in guide['end_patterns']:
                            if pattern.lower() in line_clean.lower() and len(line_clean) < 100:
                                print(f"    Found end at page {page_num}: '{line_clean}'")
                                end_page = page_num
                                break
                        if end_page is not None:
                            break
            
            # For the last guide, use all remaining pages
            if start_page is not None and end_page is None and guide_idx == len(self.guides) - 1:
                end_page = total_pages
                print(f"    Using remaining pages until {end_page}")
            
            if start_page is not None:
                page_ranges[guide['name']] = (start_page, end_page)
                print(f"    ✓ Page range: {start_page + 1} to {end_page}")
            else:
                print(f"    ✗ Could not find {guide['name']}")
        
        return page_ranges
    
    def split_pdf(self, pdf_path, output_dir):
        """Split the complete PDF into individual guides"""
        print(f"\nStep 3: Splitting PDF into individual guides...")
        
        with open(pdf_path, 'rb') as f:
            pdf_reader = PdfReader(f)
            
            # Find page ranges
            page_ranges = self.find_page_ranges(pdf_reader)
            
            # Extract each guide
            for guide in self.guides:
                if guide['name'] not in page_ranges:
                    print(f"\n  ⚠️  Skipping {guide['name']} - not found")
                    continue
                
                print(f"\n  Extracting {guide['name']}...")
                start_page, end_page = page_ranges[guide['name']]
                
                # Create new PDF
                pdf_writer = PdfWriter()
                
                # Add pages
                for page_num in range(start_page, end_page):
                    pdf_writer.add_page(pdf_reader.pages[page_num])
                
                # Add metadata
                pdf_writer.add_metadata({
                    '/Title': f"Studio3 {guide['name']}",
                    '/Author': 'Studio3 Documentation',
                    '/Subject': 'Venture Building Platform Documentation',
                    '/Creator': 'MkDocs PDF Export'
                })
                
                # Write to file
                output_path = output_dir / guide['filename']
                with open(output_path, 'wb') as output_file:
                    pdf_writer.write(output_file)
                
                # Check file size
                size_mb = output_path.stat().st_size / (1024 * 1024)
                print(f"    ✓ Created {output_path.name} ({size_mb:.1f} MB)")

def main():
    """Main function"""
    generator = PDFGenerator()
    
    # Create output directories
    site_pdf_dir = Path('site/pdf')
    site_pdf_dir.mkdir(parents=True, exist_ok=True)
    
    docs_pdf_dir = Path('docs/pdf')
    docs_pdf_dir.mkdir(parents=True, exist_ok=True)
    
    # Step 1: Generate complete PDF
    complete_pdf = generator.generate_complete_pdf()
    
    if not complete_pdf or not complete_pdf.exists():
        print("\n✗ Failed to generate complete PDF")
        print("\nTrying to use existing PDFs...")
        
        # Check if individual PDFs already exist
        existing_pdfs = list(docs_pdf_dir.glob('studio3-*-guide.pdf'))
        if existing_pdfs:
            print(f"Found {len(existing_pdfs)} existing PDFs in docs/pdf/")
            return
        else:
            print("No existing PDFs found either.")
            return
    
    # Step 2 & 3: Split into individual guides
    generator.split_pdf(complete_pdf, site_pdf_dir)
    
    # Step 4: Copy to docs/pdf
    print("\nStep 4: Copying to documentation directory...")
    import shutil
    
    for guide in generator.guides:
        src = site_pdf_dir / guide['filename']
        if src.exists():
            dst = docs_pdf_dir / guide['filename']
            shutil.copy2(src, dst)
            print(f"  ✓ Copied {guide['filename']}")
    
    # Update index
    print("\nStep 5: Updating index...")
    index_content = """# Studio3 Documentation PDFs

Professional PDF versions of all Studio3 documentation.

## Available Guides

"""
    
    for guide in generator.guides:
        pdf_path = docs_pdf_dir / guide['filename']
        if pdf_path.exists():
            size_mb = pdf_path.stat().st_size / (1024 * 1024)
            index_content += f"- [{guide['name']}]({guide['filename']}) ({size_mb:.1f} MB) - Complete guide with all sections\n"
    
    index_content += """

## Features

- Complete content from all documentation sections
- Professional formatting with MkDocs Material theme
- Syntax-highlighted code blocks  
- All diagrams and images included
- Searchable text
- Optimized for printing and digital reading

## Generation Process

These PDFs are generated using:
1. MkDocs with pdf-export plugin for complete documentation
2. Intelligent splitting based on guide structure
3. Metadata and optimization for each guide

Last updated: """ + __import__('datetime').datetime.now().strftime('%B %d, %Y')
    
    with open(docs_pdf_dir / 'index.md', 'w') as f:
        f.write(index_content)
    
    print("\n✅ PDF generation complete!")
    print(f"PDFs are available in: {docs_pdf_dir}")

if __name__ == '__main__':
    main()