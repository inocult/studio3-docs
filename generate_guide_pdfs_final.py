#!/usr/bin/env python3
"""Generate comprehensive PDF files for each guide including all subpages"""

import os
import subprocess
import yaml
import re
from pathlib import Path
from bs4 import BeautifulSoup
from weasyprint import HTML, CSS
from weasyprint.text.fonts import FontConfiguration

def load_navigation():
    """Load navigation structure from mkdocs.yml"""
    # Read the file as text first
    with open('mkdocs.yml', 'r') as f:
        content = f.read()
    
    # Remove problematic tags
    content = re.sub(r'!!python/name:[^\s]+', '{}', content)
    
    # Load YAML
    config = yaml.safe_load(content)
    return config.get('nav', [])

def extract_guide_pages(nav, guide_key):
    """Extract all pages for a specific guide from navigation"""
    pages = []
    
    def process_item(item, level=0):
        """Recursively process navigation items"""
        if isinstance(item, dict):
            for title, value in item.items():
                if isinstance(value, str):
                    # This is a page
                    pages.append({
                        'title': title,
                        'path': value,
                        'level': level
                    })
                elif isinstance(value, list):
                    # This is a section with sub-items
                    if level == 0:
                        # Add section header
                        pages.append({
                            'title': title,
                            'path': None,
                            'level': level
                        })
                    for sub_item in value:
                        process_item(sub_item, level + 1)
    
    # Find the guide in navigation
    for nav_item in nav:
        if isinstance(nav_item, dict):
            for key, value in nav_item.items():
                if guide_key.lower() in key.lower():
                    # Found the guide section
                    if isinstance(value, str):
                        # Guide has only index page
                        pages.append({
                            'title': key,
                            'path': value,
                            'level': 0
                        })
                    elif isinstance(value, list):
                        # Guide has sub-sections
                        for item in value:
                            process_item(item, 0)
                    break
    
    return pages

def read_html_content(page_path):
    """Read and process HTML content from built site"""
    if not page_path:
        return None
        
    html_path = Path('site') / page_path.replace('.md', '/index.html')
    
    if not html_path.exists():
        # Try without index.html
        html_path = Path('site') / page_path.replace('.md', '.html')
    
    if not html_path.exists():
        print(f"    Warning: {html_path} not found")
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
        
        # Remove pagination links
        for elem in main_content.find_all('div', class_='md-source-file'):
            elem.decompose()
            
        return str(main_content)
    
    return None

def create_combined_html(guide_name, pages, site_url='file:///home/inocult/projects/studio3-docs/site/'):
    """Create a combined HTML document with all guide pages"""
    
    html_parts = [f'''
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Studio3 {guide_name} Guide</title>
    <link rel="stylesheet" href="{site_url}assets/stylesheets/main.e4a7b2b8.min.css">
    <link rel="stylesheet" href="{site_url}stylesheets/extra.css">
    <style>
        /* PDF-specific styles */
        @media print {{
            body {{
                font-size: 11pt;
                line-height: 1.6;
                color: #000;
                background: white;
            }}
            
            /* Hide navigation and interactive elements */
            .md-header, .md-sidebar, .md-footer, .md-top, 
            .md-search, .md-tabs, button, .md-button {{
                display: none !important;
            }}
            
            /* Full width content */
            .md-content {{
                max-width: 100% !important;
                margin: 0 !important;
                padding: 0 !important;
            }}
            
            .md-content__inner {{
                margin: 0 !important;
                padding: 0 !important;
            }}
            
            /* Page breaks */
            h1 {{
                page-break-before: always;
                margin-top: 0;
            }}
            
            h1:first-child {{
                page-break-before: avoid;
            }}
            
            h2, h3, h4 {{
                page-break-after: avoid;
            }}
            
            /* Keep elements together */
            .arena-card, .admonition, blockquote, pre, table {{
                page-break-inside: avoid;
            }}
            
            /* Fix margins */
            p, ul, ol {{
                orphans: 3;
                widows: 3;
            }}
            
            /* Table of contents */
            .pdf-toc {{
                page-break-after: always;
            }}
            
            .pdf-toc ul {{
                list-style: none;
                padding-left: 0;
            }}
            
            .pdf-toc li {{
                margin: 8pt 0;
            }}
            
            .pdf-toc li.level-1 {{
                font-weight: bold;
                margin-top: 12pt;
            }}
            
            .pdf-toc li.level-2 {{
                margin-left: 20pt;
            }}
            
            .pdf-toc li.level-3 {{
                margin-left: 40pt;
            }}
            
            /* Title page */
            .pdf-title-page {{
                text-align: center;
                page-break-after: always;
                min-height: 100vh;
                display: flex;
                flex-direction: column;
                justify-content: center;
            }}
            
            .pdf-title-page h1 {{
                font-size: 48pt;
                margin-bottom: 40pt;
                page-break-before: avoid;
            }}
            
            .pdf-title-page .subtitle {{
                font-size: 18pt;
                color: #666;
                margin-bottom: 20pt;
            }}
            
            .pdf-title-page .date {{
                font-size: 14pt;
                color: #999;
                position: absolute;
                bottom: 50pt;
                left: 0;
                right: 0;
            }}
        }}
        
        /* Ensure content is visible */
        .md-content {{
            display: block !important;
        }}
        
        /* Fix code blocks */
        pre {{
            white-space: pre-wrap;
            word-wrap: break-word;
        }}
        
        /* Fix images */
        img {{
            max-width: 100%;
            height: auto;
        }}
    </style>
</head>
<body>
<div class="md-content">
''']
    
    # Add title page
    from datetime import datetime
    current_date = datetime.now().strftime("%B %Y")
    
    html_parts.append(f'''
    <div class="pdf-title-page">
        <h1>Studio3 {guide_name} Guide</h1>
        <p class="subtitle">The Complete Reference</p>
        <p class="date">{current_date}</p>
    </div>
    ''')
    
    # Add table of contents if we have multiple pages
    if len([p for p in pages if p['path']]) > 1:
        html_parts.append('''
        <div class="pdf-toc">
            <h1>Table of Contents</h1>
            <ul>
        ''')
        
        for page in pages:
            if page['path'] or page['level'] == 0:
                level_class = f'level-{page["level"]}'
                html_parts.append(f'<li class="{level_class}">{page["title"]}</li>\n')
        
        html_parts.append('</ul></div>')
    
    # Add all pages content
    for i, page in enumerate(pages):
        if page['path']:
            print(f"  Processing: {page['title']}...")
            content = read_html_content(page['path'])
            
            if content:
                # Add page break before major sections
                if page['level'] == 0 and i > 0:
                    html_parts.append('<div style="page-break-before: always;"></div>')
                
                # Process content to fix relative URLs
                content = content.replace('href="../', f'href="{site_url}')
                content = content.replace('src="../', f'src="{site_url}')
                content = content.replace('href="../../', f'href="{site_url}')
                content = content.replace('src="../../', f'src="{site_url}')
                
                html_parts.append(content)
        elif page['level'] == 0 and page['title']:
            # Section header without content
            html_parts.append(f'<h1>{page["title"]}</h1>')
    
    html_parts.append('</div></body></html>')
    
    return ''.join(html_parts)

def generate_pdf_from_html(html_content, output_path, guide_name):
    """Generate PDF from HTML content using weasyprint"""
    
    # Custom CSS for PDF generation
    pdf_css = CSS(string=f'''
        @page {{
            size: A4;
            margin: 2.5cm 2cm 3cm 2cm;
            
            @bottom-center {{
                content: "{guide_name} Guide - Page " counter(page) " of " counter(pages);
                font-size: 10pt;
                color: #666;
            }}
        }}
        
        @page:first {{
            @bottom-center {{
                content: "";
            }}
        }}
        
        @page:blank {{
            @bottom-center {{
                content: "";
            }}
        }}
    ''')
    
    try:
        # Configure fonts
        font_config = FontConfiguration()
        
        # Write HTML for debugging
        debug_html = Path(f'debug_{guide_name.lower()}.html')
        with open(debug_html, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        # Generate PDF
        HTML(string=html_content, base_url=str(Path('site').absolute())).write_pdf(
            output_path,
            stylesheets=[pdf_css],
            font_config=font_config
        )
        
        # Remove debug HTML
        debug_html.unlink()
        
        return True
    except Exception as e:
        print(f"  Error generating PDF: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Generate comprehensive PDFs for each guide"""
    
    # First ensure the site is built with PDF export enabled
    if not Path('site').exists():
        print("Site directory not found. Building site first...")
        env = os.environ.copy()
        env['ENABLE_PDF_EXPORT'] = '1'
        subprocess.run(['mkdocs', 'build'], check=True, env=env)
    
    # Load navigation
    nav = load_navigation()
    
    # Define guides to generate
    guides = [
        {
            'name': 'Overview',
            'nav_key': 'Overview Guide',
            'output': 'studio3-overview-guide.pdf'
        },
        {
            'name': 'Senders',
            'nav_key': 'Senders Guide',
            'output': 'studio3-senders-guide.pdf'
        },
        {
            'name': 'Echoes',
            'nav_key': 'Echoes Guide',
            'output': 'studio3-echoes-guide.pdf'
        },
        {
            'name': 'Anchors',
            'nav_key': 'Anchors Guide',
            'output': 'studio3-anchors-guide.pdf'
        }
    ]
    
    # Create PDF directory
    pdf_dir = Path('site/pdf')
    pdf_dir.mkdir(parents=True, exist_ok=True)
    
    # Also create docs/pdf directory
    docs_pdf_dir = Path('docs/pdf')
    docs_pdf_dir.mkdir(parents=True, exist_ok=True)
    
    success_count = 0
    
    for guide in guides:
        print(f"\nGenerating comprehensive PDF for {guide['name']} Guide...")
        
        # Extract all pages for this guide
        pages = extract_guide_pages(nav, guide['nav_key'])
        print(f"  Found {len(pages)} sections/pages")
        
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
            
            # Copy to docs/pdf
            import shutil
            docs_pdf_path = docs_pdf_dir / guide['output']
            shutil.copy2(output_path, docs_pdf_path)
            print(f"  Copied to {docs_pdf_path}")
            
            success_count += 1
        else:
            print(f"✗ Failed to generate {output_path}")
    
    print(f"\n✅ Generated {success_count}/{len(guides)} PDFs successfully")
    
    # Create a simple index of PDFs
    index_content = "# PDF Guides\n\n"
    for guide in guides:
        pdf_path = docs_pdf_dir / guide['output']
        if pdf_path.exists():
            size_mb = pdf_path.stat().st_size / (1024 * 1024)
            index_content += f"- [{guide['name']} Guide]({guide['output']}) ({size_mb:.1f} MB)\n"
    
    with open(docs_pdf_dir / 'index.md', 'w') as f:
        f.write(index_content)

if __name__ == '__main__':
    main()