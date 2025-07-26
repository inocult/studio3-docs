#!/usr/bin/env python3
"""Generate individual PDF files for each guide using weasyprint"""

import os
import subprocess
from pathlib import Path
from weasyprint import HTML, CSS
from weasyprint.text.fonts import FontConfiguration

def create_guide_html(guide_name, guide_path, site_url='https://inocult.github.io/studio3-docs/'):
    """Create a combined HTML file for a guide by reading its index page"""
    
    # Read the built HTML file from the site directory
    html_path = Path('site') / guide_path / 'index.html'
    
    if not html_path.exists():
        print(f"Warning: {html_path} not found")
        return None
        
    with open(html_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # Fix relative URLs to absolute
    html_content = html_content.replace('href="../', f'href="{site_url}')
    html_content = html_content.replace('src="../', f'src="{site_url}')
    html_content = html_content.replace('href="../../', f'href="{site_url}')
    html_content = html_content.replace('src="../../', f'src="{site_url}')
    
    return html_content

def generate_pdf_from_html(html_content, output_path, guide_name):
    """Generate PDF from HTML content using weasyprint"""
    
    # Custom CSS for PDF generation
    pdf_css = CSS(string='''
        @page {
            size: A4;
            margin: 2cm;
            @bottom-center {
                content: "Studio3 " + ''' + f'"{guide_name} Guide"' + ''' + " - Page " counter(page);
                font-size: 10pt;
                color: #666;
            }
        }
        
        /* Hide navigation and header for PDF */
        .md-header, .md-sidebar, .md-footer, .md-top {
            display: none !important;
        }
        
        /* Adjust content width for PDF */
        .md-content {
            max-width: 100% !important;
            margin: 0 !important;
            padding: 0 !important;
        }
        
        .md-content__inner {
            margin: 0 !important;
            padding: 0 !important;
        }
        
        /* Improve print styles */
        body {
            font-size: 11pt;
            line-height: 1.6;
            color: #000;
            background: white;
        }
        
        h1, h2, h3, h4, h5, h6 {
            page-break-after: avoid;
            margin-top: 1.5em;
        }
        
        h1 { font-size: 24pt; }
        h2 { font-size: 18pt; }
        h3 { font-size: 14pt; }
        
        pre, blockquote {
            page-break-inside: avoid;
        }
        
        .arena-card {
            page-break-inside: avoid;
            border: 1px solid #ddd;
            padding: 1em;
            margin: 1em 0;
            background: #f9f9f9;
        }
        
        /* Hide buttons in PDF */
        .md-button {
            display: none !important;
        }
        
        /* Fix admonitions for print */
        .admonition {
            border: 1px solid #ddd;
            padding: 0.5em 1em;
            margin: 1em 0;
            page-break-inside: avoid;
        }
    ''')
    
    try:
        # Configure fonts
        font_config = FontConfiguration()
        
        # Generate PDF
        HTML(string=html_content).write_pdf(
            output_path,
            stylesheets=[pdf_css],
            font_config=font_config
        )
        
        return True
    except Exception as e:
        print(f"Error generating PDF: {e}")
        return False

def main():
    """Generate individual PDFs for each guide"""
    
    # First ensure the site is built
    if not Path('site').exists():
        print("Site directory not found. Building site first...")
        subprocess.run(['mkdocs', 'build'], check=True)
    
    # Define guides
    guides = [
        {
            'name': 'Overview',
            'path': 'overview-guide',
            'output': 'overview-guide.pdf'
        },
        {
            'name': 'Senders',
            'path': 'senders-guide',
            'output': 'senders-guide.pdf'
        },
        {
            'name': 'Echoes',
            'path': 'echoes-guide',
            'output': 'echoes-guide.pdf'
        },
        {
            'name': 'Anchors',
            'path': 'anchors-guide',
            'output': 'anchors-guide.pdf'
        }
    ]
    
    # Create PDF directory
    pdf_dir = Path('site/pdf')
    pdf_dir.mkdir(parents=True, exist_ok=True)
    
    success_count = 0
    
    for guide in guides:
        print(f"\nGenerating PDF for {guide['name']} Guide...")
        
        # Get HTML content
        html_content = create_guide_html(guide['name'], guide['path'])
        if not html_content:
            continue
        
        # Generate PDF
        output_path = pdf_dir / guide['output']
        if generate_pdf_from_html(html_content, str(output_path), guide['name']):
            print(f"✓ Generated {output_path}")
            success_count += 1
        else:
            print(f"✗ Failed to generate {output_path}")
    
    print(f"\nGenerated {success_count}/{len(guides)} PDFs successfully")

if __name__ == '__main__':
    main()