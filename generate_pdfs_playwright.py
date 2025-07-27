#!/usr/bin/env python3
"""Generate high-quality PDFs using Playwright to render the actual site"""

import asyncio
import subprocess
from pathlib import Path
from playwright.async_api import async_playwright
import yaml
import re

def load_navigation():
    """Load navigation structure from mkdocs.yml"""
    with open('mkdocs.yml', 'r') as f:
        content = f.read()
    
    # Remove problematic tags
    content = re.sub(r'!!python/name:[^\s]+', '{}', content)
    
    # Load YAML
    config = yaml.safe_load(content)
    return config.get('nav', [])

def extract_guide_urls(nav, guide_key, base_url='http://localhost:8000/'):
    """Extract all page URLs for a specific guide"""
    urls = []
    
    def process_item(item, parent_path=""):
        """Recursively process navigation items"""
        if isinstance(item, dict):
            for title, value in item.items():
                if isinstance(value, str):
                    # This is a page - convert path to URL
                    url_path = value.replace('.md', '/')
                    urls.append({
                        'title': title,
                        'url': base_url + url_path
                    })
                elif isinstance(value, list):
                    # This is a section with sub-items
                    for sub_item in value:
                        process_item(sub_item, parent_path)
    
    # Find the guide in navigation
    for nav_item in nav:
        if isinstance(nav_item, dict):
            for key, value in nav_item.items():
                if guide_key.lower() in key.lower():
                    # Found the guide section
                    if isinstance(value, str):
                        # Guide has only index page
                        url_path = value.replace('.md', '/')
                        urls.append({
                            'title': key,
                            'url': base_url + url_path
                        })
                    elif isinstance(value, list):
                        # Guide has sub-sections
                        for item in value:
                            process_item(item)
                    break
    
    return urls

async def generate_guide_pdf(page, guide_name, urls, output_path):
    """Generate a single PDF containing all pages of a guide"""
    
    print(f"\nGenerating {guide_name} Guide PDF...")
    
    # Create a temporary HTML file that combines all pages
    combined_html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Studio3 {guide_name} Guide</title>
    <style>
        /* Import all MkDocs styles */
        @import url('http://localhost:8000/assets/stylesheets/main.e4a7b2b8.min.css');
        @import url('http://localhost:8000/stylesheets/extra.css');
        
        /* PDF-specific overrides */
        @media print {{
            /* Hide navigation elements */
            .md-header, .md-tabs, .md-nav, .md-sidebar, 
            .md-footer, .md-top, .md-search {{
                display: none !important;
            }}
            
            /* Full width content */
            .md-main, .md-content {{
                max-width: 100% !important;
            }}
            
            .md-grid {{
                max-width: 100% !important;
                margin: 0 !important;
            }}
            
            .md-content__inner {{
                margin: 0 !important;
                padding: 20px !important;
            }}
            
            /* Page breaks */
            .page-section {{
                page-break-before: always;
            }}
            
            .page-section:first-child {{
                page-break-before: avoid;
            }}
            
            /* Keep elements together */
            h1, h2, h3, h4, h5, h6 {{
                page-break-after: avoid;
            }}
            
            .arena-card, .admonition, pre, blockquote {{
                page-break-inside: avoid;
            }}
            
            /* Fix backgrounds */
            body {{
                background: white !important;
                color: black !important;
            }}
            
            /* Better link printing */
            a {{
                color: #1976d2 !important;
            }}
            
            /* Show URLs for external links */
            a[href^="http"]:not([href*="localhost"]):not([href*="studio3-docs"]):after {{
                content: " (" attr(href) ")";
                font-size: 0.8em;
                color: #666;
            }}
        }}
        
        /* Title page */
        .title-page {{
            text-align: center;
            padding: 200px 0;
            page-break-after: always;
        }}
        
        .title-page h1 {{
            font-size: 48pt;
            color: #2B4C8C;
            margin-bottom: 30px;
        }}
        
        .title-page .subtitle {{
            font-size: 18pt;
            color: #666;
        }}
        
        /* Table of contents */
        .toc-page {{
            page-break-after: always;
            padding: 40px;
        }}
        
        .toc-page h2 {{
            color: #2B4C8C;
            border-bottom: 3px solid #E91E63;
            padding-bottom: 10px;
            margin-bottom: 30px;
        }}
        
        .toc-page ul {{
            list-style: none;
            padding-left: 0;
        }}
        
        .toc-page li {{
            margin: 10px 0;
            font-size: 12pt;
        }}
        
        .toc-page li a {{
            text-decoration: none;
            color: #333;
        }}
        
        .toc-page li a:hover {{
            color: #E91E63;
        }}
        
        /* Page sections */
        .page-section {{
            min-height: 100vh;
            padding: 40px;
        }}
    </style>
</head>
<body>
    <!-- Title Page -->
    <div class="title-page">
        <h1>Studio3 {guide_name} Guide</h1>
        <p class="subtitle">Complete Reference Documentation</p>
    </div>
    
    <!-- Table of Contents -->
    <div class="toc-page">
        <h2>Table of Contents</h2>
        <ul>
"""
    
    # Add TOC entries
    for i, page_info in enumerate(urls):
        combined_html += f'            <li><a href="#section-{i}">{page_info["title"]}</a></li>\n'
    
    combined_html += """
        </ul>
    </div>
    
    <!-- Content Pages -->
"""
    
    # Load and combine all pages
    for i, page_info in enumerate(urls):
        print(f"  Loading {page_info['title']}...")
        
        # Navigate to the page
        await page.goto(page_info['url'], wait_until='networkidle')
        
        # Wait for content to render
        await page.wait_for_selector('.md-content', state='visible')
        
        # Extract the main content
        content = await page.evaluate('''() => {
            const content = document.querySelector('.md-content__inner');
            if (content) {
                // Remove any remaining navigation elements
                const navElements = content.querySelectorAll('.md-nav, .md-sidebar__scrollwrap');
                navElements.forEach(el => el.remove());
                
                // Fix relative links
                const links = content.querySelectorAll('a[href^="../"]');
                links.forEach(link => {
                    link.href = link.href.replace(/\.\.\//g, '');
                });
                
                return content.innerHTML;
            }
            return '';
        }''')
        
        # Add to combined HTML
        combined_html += f'''
    <div id="section-{i}" class="page-section">
        <div class="md-content">
            <article class="md-content__inner md-typeset">
                {content}
            </article>
        </div>
    </div>
'''
    
    combined_html += """
</body>
</html>
"""
    
    # Create temporary HTML file
    temp_html = Path(f'temp_{guide_name.lower()}_combined.html')
    with open(temp_html, 'w', encoding='utf-8') as f:
        f.write(combined_html)
    
    # Navigate to the combined HTML
    await page.goto(f'file://{temp_html.absolute()}', wait_until='networkidle')
    
    # Generate PDF with proper settings
    await page.pdf(
        path=str(output_path),
        format='A4',
        print_background=True,
        margin={
            'top': '20mm',
            'right': '20mm',
            'bottom': '30mm',
            'left': '20mm'
        },
        display_header_footer=True,
        header_template='<div></div>',
        footer_template='''
            <div style="width: 100%; font-size: 10px; text-align: center; color: #666;">
                <span>Studio3 ''' + guide_name + ''' Guide - Page <span class="pageNumber"></span> of <span class="totalPages"></span></span>
            </div>
        '''
    )
    
    # Clean up temp file
    temp_html.unlink()
    
    print(f"  ✓ Generated {output_path}")
    return True

async def main():
    """Generate PDFs for all guides"""
    
    # First ensure the site is built and served
    print("Starting MkDocs server...")
    server_process = subprocess.Popen(
        ['mkdocs', 'serve', '--no-livereload'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    # Wait for server to start
    await asyncio.sleep(3)
    
    try:
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
        
        # Create output directories
        pdf_dir = Path('site/pdf')
        pdf_dir.mkdir(parents=True, exist_ok=True)
        
        docs_pdf_dir = Path('docs/pdf')
        docs_pdf_dir.mkdir(parents=True, exist_ok=True)
        
        async with async_playwright() as p:
            # Launch browser
            browser = await p.chromium.launch(
                headless=True,
                args=['--no-sandbox', '--disable-setuid-sandbox']
            )
            
            # Create context with viewport
            context = await browser.new_context(
                viewport={'width': 1280, 'height': 800}
            )
            
            # Create page
            page = await context.new_page()
            
            # Generate each guide
            for guide in guides:
                # Extract URLs for this guide
                urls = extract_guide_urls(nav, guide['nav_key'])
                
                if not urls:
                    print(f"No pages found for {guide['name']} Guide")
                    continue
                
                print(f"Found {len(urls)} pages for {guide['name']} Guide")
                
                # Generate PDF
                output_path = pdf_dir / guide['output']
                await generate_guide_pdf(page, guide['name'], urls, output_path)
                
                # Copy to docs/pdf
                import shutil
                docs_path = docs_pdf_dir / guide['output']
                shutil.copy2(output_path, docs_path)
                print(f"  ✓ Copied to {docs_path}")
                
                # Check file size
                size_mb = output_path.stat().st_size / (1024 * 1024)
                print(f"  Size: {size_mb:.1f} MB")
            
            await browser.close()
    
    finally:
        # Stop the server
        server_process.terminate()
        server_process.wait()
        print("\nMkDocs server stopped")

if __name__ == '__main__':
    asyncio.run(main())