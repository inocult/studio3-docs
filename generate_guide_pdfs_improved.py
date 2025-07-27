#!/usr/bin/env python3
"""Generate comprehensive PDF files for each guide including all subpages"""

import os
import subprocess
import yaml
from pathlib import Path
from bs4 import BeautifulSoup
from weasyprint import HTML, CSS
from weasyprint.text.fonts import FontConfiguration

def load_navigation():
    """Load navigation structure from mkdocs.yml"""
    import re
    
    # Read the file as text first
    with open('mkdocs.yml', 'r') as f:
        content = f.read()
    
    # Remove problematic tags
    content = re.sub(r'!!python/name:[^\s]+', '{}', content)
    
    # Load YAML
    config = yaml.safe_load(content)
    return config.get('nav', [])

def extract_guide_pages(nav, guide_name):
    """Extract all pages for a specific guide from navigation"""
    pages = []
    
    def process_nav_item(item, current_path=""):
        if isinstance(item, dict):
            for key, value in item.items():
                if isinstance(value, list):
                    # This is a section with sub-items
                    for sub_item in value:
                        process_nav_item(sub_item, current_path)
                elif isinstance(value, str):
                    # This is a page
                    if guide_name in value:
                        pages.append({
                            'title': key,
                            'path': value,
                            'level': current_path.count('/') + 1
                        })
    
    # Find the guide section in navigation
    for item in nav:
        if isinstance(item, dict):
            for key, value in item.items():
                if guide_name in key.lower():
                    # Process all items in this guide section
                    if isinstance(value, list):
                        for sub_item in value:
                            process_nav_item(sub_item)
                    elif isinstance(value, str):
                        pages.append({
                            'title': key,
                            'path': value,
                            'level': 0
                        })
    
    return pages

def read_html_content(page_path):
    """Read and process HTML content from built site"""
    html_path = Path('site') / page_path.replace('.md', '/index.html')
    
    if not html_path.exists():
        # Try without index.html
        html_path = Path('site') / page_path.replace('.md', '.html')
    
    if not html_path.exists():
        print(f"Warning: {html_path} not found")
        return None
    
    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Parse HTML to extract main content
    soup = BeautifulSoup(content, 'html.parser')
    
    # Find main content area
    main_content = soup.find('article', class_='md-content__inner')
    if not main_content:
        main_content = soup.find('div', class_='md-content')
    
    if main_content:
        # Remove navigation elements
        for elem in main_content.find_all(['nav', 'a'], class_=['md-nav', 'md-content__button']):
            elem.decompose()
        
        return str(main_content)
    
    return None

def create_combined_html(guide_name, pages, site_url='https://inocult.github.io/studio3-docs/'):
    """Create a combined HTML document with all guide pages"""
    
    html_parts = ['''
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Studio3 ''' + guide_name + ''' Guide</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 210mm;
            margin: 0 auto;
            padding: 20px;
        }
        
        h1 { 
            font-size: 28pt; 
            margin-top: 0;
            page-break-before: always;
        }
        
        h1:first-child {
            page-break-before: avoid;
        }
        
        h2 { 
            font-size: 20pt; 
            margin-top: 30pt;
            page-break-after: avoid;
        }
        
        h3 { 
            font-size: 16pt; 
            margin-top: 24pt;
            page-break-after: avoid;
        }
        
        h4 { 
            font-size: 14pt; 
            margin-top: 20pt;
            page-break-after: avoid;
        }
        
        /* Prevent widows and orphans */
        p {
            orphans: 3;
            widows: 3;
        }
        
        /* Keep elements together */
        .arena-card, .admonition, blockquote, pre {
            page-break-inside: avoid;
        }
        
        /* Table of Contents */
        .toc {
            page-break-after: always;
            margin-bottom: 40pt;
        }
        
        .toc h2 {
            font-size: 24pt;
            margin-bottom: 20pt;
        }
        
        .toc ul {
            list-style: none;
            padding-left: 0;
        }
        
        .toc li {
            margin: 8pt 0;
            line-height: 1.8;
        }
        
        .toc a {
            text-decoration: none;
            color: #333;
            display: flex;
            justify-content: space-between;
        }
        
        .toc .page-num {
            color: #666;
        }
        
        /* Arena cards */
        .arena-card {
            border: 1px solid #e0e0e0;
            border-radius: 8px;
            padding: 16pt;
            margin: 16pt 0;
            background: #f8f9fa;
        }
        
        /* Admonitions */
        .admonition {
            border-left: 4px solid #448aff;
            padding: 12pt 16pt;
            margin: 16pt 0;
            background: #f0f7ff;
        }
        
        .admonition.warning {
            border-color: #ff9800;
            background: #fff8e1;
        }
        
        .admonition.success {
            border-color: #4caf50;
            background: #f1f8f4;
        }
        
        /* Code blocks */
        pre {
            background: #f5f5f5;
            padding: 12pt;
            border-radius: 4px;
            overflow-x: auto;
            font-size: 10pt;
        }
        
        code {
            background: #f5f5f5;
            padding: 2pt 4pt;
            border-radius: 2px;
            font-size: 10pt;
        }
        
        /* Tables */
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 16pt 0;
            page-break-inside: auto;
        }
        
        th, td {
            border: 1px solid #ddd;
            padding: 8pt;
            text-align: left;
        }
        
        th {
            background: #f5f5f5;
            font-weight: bold;
        }
        
        tr {
            page-break-inside: avoid;
        }
        
        /* Images */
        img {
            max-width: 100%;
            height: auto;
        }
        
        /* Hide interactive elements */
        button, .md-button, .md-tabs, .md-search {
            display: none !important;
        }
    </style>
</head>
<body>
''']
    
    # Add title page
    html_parts.append(f'''
    <div style="text-align: center; margin-top: 200pt;">
        <h1 style="font-size: 48pt; page-break-before: avoid;">Studio3 {guide_name} Guide</h1>
        <p style="font-size: 16pt; margin-top: 40pt;">The Complete Reference</p>
        <p style="font-size: 14pt; margin-top: 200pt;">Generated from studio3-docs.github.io</p>
    </div>
    ''')
    
    # Add table of contents
    html_parts.append('''
    <div class="toc">
        <h2>Table of Contents</h2>
        <ul>
    ''')
    
    for i, page in enumerate(pages):
        indent = '    ' * page['level']
        html_parts.append(f'{indent}<li><a href="#{i}">{page["title"]}<span class="page-num"></span></a></li>\n')
    
    html_parts.append('</ul></div>')
    
    # Add all pages content
    for i, page in enumerate(pages):
        print(f"  Adding {page['title']}...")
        content = read_html_content(page['path'])
        
        if content:
            # Add section marker
            html_parts.append(f'<div id="{i}" class="section">')
            
            # Process content to fix relative URLs
            content = content.replace('href="../', f'href="{site_url}')
            content = content.replace('src="../', f'src="{site_url}')
            content = content.replace('href="../../', f'href="{site_url}')
            content = content.replace('src="../../', f'src="{site_url}')
            
            html_parts.append(content)
            html_parts.append('</div>')
    
    html_parts.append('</body></html>')
    
    return ''.join(html_parts)

def generate_pdf_from_html(html_content, output_path, guide_name):
    """Generate PDF from HTML content using weasyprint"""
    
    # Custom CSS for PDF generation
    pdf_css = CSS(string='''
        @page {
            size: A4;
            margin: 2.5cm 2cm 3cm 2cm;
            
            @bottom-center {
                content: "Studio3 ''' + guide_name + ''' Guide - Page " counter(page);
                font-size: 10pt;
                color: #666;
            }
            
            @bottom-right {
                content: counter(page);
                font-size: 10pt;
                color: #666;
            }
        }
        
        @page:first {
            @bottom-center {
                content: "";
            }
            @bottom-right {
                content: "";
            }
        }
        
        /* Ensure no blank pages between sections */
        .section {
            page-break-before: auto;
        }
        
        .section:first-child {
            page-break-before: avoid;
        }
        
        /* Fix heading spacing */
        h1, h2, h3, h4, h5, h6 {
            margin-bottom: 0.5em;
        }
        
        h1 + *, h2 + *, h3 + * {
            margin-top: 0.5em;
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
    """Generate comprehensive PDFs for each guide"""
    
    # First ensure the site is built
    if not Path('site').exists():
        print("Site directory not found. Building site first...")
        subprocess.run(['mkdocs', 'build'], check=True)
    
    # Load navigation
    nav = load_navigation()
    
    # Define guides to generate
    guides = [
        {
            'name': 'Overview',
            'search_name': 'overview guide',
            'output': 'studio3-overview-guide.pdf'
        },
        {
            'name': 'Senders',
            'search_name': 'senders guide',
            'output': 'studio3-senders-guide.pdf'
        },
        {
            'name': 'Echoes',
            'search_name': 'echoes guide',
            'output': 'studio3-echoes-guide.pdf'
        },
        {
            'name': 'Anchors',
            'search_name': 'anchors guide',
            'output': 'studio3-anchors-guide.pdf'
        }
    ]
    
    # Create PDF directory
    pdf_dir = Path('site/pdf')
    pdf_dir.mkdir(parents=True, exist_ok=True)
    
    success_count = 0
    
    for guide in guides:
        print(f"\nGenerating comprehensive PDF for {guide['name']} Guide...")
        
        # Extract all pages for this guide
        pages = extract_guide_pages(nav, guide['search_name'])
        print(f"  Found {len(pages)} pages")
        
        if not pages:
            print(f"  No pages found for {guide['name']} Guide")
            continue
        
        # Create combined HTML
        html_content = create_combined_html(guide['name'], pages)
        
        # Generate PDF
        output_path = pdf_dir / guide['output']
        if generate_pdf_from_html(html_content, str(output_path), guide['name']):
            print(f"✓ Generated {output_path}")
            # Check file size
            size_mb = output_path.stat().st_size / (1024 * 1024)
            print(f"  Size: {size_mb:.1f} MB")
            success_count += 1
        else:
            print(f"✗ Failed to generate {output_path}")
    
    print(f"\nGenerated {success_count}/{len(guides)} PDFs successfully")
    
    # Copy PDFs to docs/pdf for direct access
    docs_pdf_dir = Path('docs/pdf')
    docs_pdf_dir.mkdir(parents=True, exist_ok=True)
    
    for pdf_file in pdf_dir.glob('*.pdf'):
        target = docs_pdf_dir / pdf_file.name
        import shutil
        shutil.copy2(pdf_file, target)
        print(f"Copied {pdf_file.name} to docs/pdf/")

if __name__ == '__main__':
    main()