#!/usr/bin/env python3
"""
Comprehensive PDF generation for Studio3 documentation
Combines all pages of each guide into high-quality PDFs
"""

import os
import subprocess
import time
import yaml
import re
from pathlib import Path
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup

class PDFGenerator:
    def __init__(self, base_url='http://localhost:8000/'):
        self.base_url = base_url
        self.session = requests.Session()
        
    def load_navigation(self):
        """Load navigation structure from mkdocs.yml"""
        with open('mkdocs.yml', 'r') as f:
            content = f.read()
        
        # Remove problematic tags
        content = re.sub(r'!!python/name:[^\s]+', '{}', content)
        
        # Load YAML
        config = yaml.safe_load(content)
        return config.get('nav', [])
    
    def extract_guide_pages(self, nav, guide_key):
        """Extract all pages for a specific guide from navigation"""
        pages = []
        
        def process_item(item, level=0, section_title=""):
            """Recursively process navigation items"""
            if isinstance(item, dict):
                for title, value in item.items():
                    if isinstance(value, str):
                        # This is a page
                        pages.append({
                            'title': title,
                            'path': value,
                            'level': level,
                            'section': section_title
                        })
                    elif isinstance(value, list):
                        # This is a section with sub-items
                        new_section = section_title
                        if level > 0:
                            new_section = title
                        for sub_item in value:
                            process_item(sub_item, level + 1, new_section)
        
        # Find the guide in navigation
        for nav_item in nav:
            if isinstance(nav_item, dict):
                for key, value in nav_item.items():
                    if guide_key.lower() in key.lower():
                        # Found the guide section
                        if isinstance(value, str):
                            pages.append({
                                'title': key,
                                'path': value,
                                'level': 0,
                                'section': ''
                            })
                        elif isinstance(value, list):
                            for item in value:
                                process_item(item, 1, "")
                        break
        
        return pages
    
    def fetch_page_content(self, page_path):
        """Fetch and process page content from the live server"""
        # Convert path to URL
        url = urljoin(self.base_url, page_path.replace('.md', '/'))
        
        try:
            response = self.session.get(url)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Find main content
            content = soup.find('article', class_='md-content__inner')
            if not content:
                content = soup.find('div', class_='md-content')
            
            if content:
                # Remove navigation elements
                for elem in content.find_all(['nav', 'a'], class_=['md-nav', 'md-content__button']):
                    elem.decompose()
                
                # Fix relative URLs
                for tag in content.find_all(['a', 'img']):
                    if tag.name == 'a' and tag.get('href'):
                        if tag['href'].startswith('../'):
                            tag['href'] = urljoin(url, tag['href'])
                    elif tag.name == 'img' and tag.get('src'):
                        if tag['src'].startswith('../'):
                            tag['src'] = urljoin(url, tag['src'])
                
                return str(content)
            
        except Exception as e:
            print(f"    Error fetching {url}: {e}")
        
        return None
    
    def generate_combined_html(self, guide_name, pages):
        """Generate a combined HTML document for the entire guide"""
        
        # Start with HTML template
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Studio3 {guide_name} Guide</title>
    
    <!-- MkDocs Material CSS -->
    <link rel="stylesheet" href="{self.base_url}assets/stylesheets/main.e4a7b2b8.min.css">
    <link rel="stylesheet" href="{self.base_url}assets/stylesheets/palette.e464397b.min.css">
    
    <!-- Custom CSS -->
    <link rel="stylesheet" href="{self.base_url}stylesheets/extra.css">
    <link rel="stylesheet" href="{self.base_url}stylesheets/pdf-enhanced.css">
    
    <!-- Fonts -->
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Roboto:300,300i,400,400i,700,700i%7CRoboto+Mono:400,400i,700,700i&display=fallback">
    <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Rubik:wght@400;500;600;700&family=Source+Sans+Pro:wght@400;600;700&display=swap">
    
    <style>
        /* Override for PDF generation */
        body {{ 
            background: white !important; 
            padding: 0;
            margin: 0;
        }}
        
        .md-container {{
            background: white !important;
        }}
        
        .md-main {{
            margin: 0;
            padding: 0;
        }}
        
        .md-content {{
            max-width: none !important;
            margin: 0 !important;
            padding: 20px 40px !important;
        }}
        
        /* Title page */
        .pdf-title-page {{
            text-align: center;
            padding: 150px 40px;
            page-break-after: always;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
        }}
        
        .pdf-title-page h1 {{
            font-size: 48px;
            color: #2B4C8C;
            margin-bottom: 20px;
            font-family: 'Rubik', sans-serif;
        }}
        
        .pdf-title-page .subtitle {{
            font-size: 24px;
            color: #666;
            margin-bottom: 60px;
        }}
        
        .pdf-title-page .date {{
            font-size: 16px;
            color: #999;
        }}
        
        /* Table of contents */
        .pdf-toc {{
            page-break-after: always;
            padding: 40px;
            min-height: 100vh;
        }}
        
        .pdf-toc h2 {{
            color: #2B4C8C;
            font-size: 32px;
            margin-bottom: 40px;
            font-family: 'Rubik', sans-serif;
        }}
        
        .pdf-toc ul {{
            list-style: none;
            padding: 0;
            margin: 0;
        }}
        
        .pdf-toc > ul > li {{
            margin-bottom: 20px;
        }}
        
        .pdf-toc .toc-section {{
            font-weight: 600;
            font-size: 18px;
            color: #2B4C8C;
            margin-bottom: 10px;
        }}
        
        .pdf-toc .toc-page {{
            margin-left: 20px;
            margin-bottom: 8px;
            font-size: 16px;
        }}
        
        .pdf-toc a {{
            text-decoration: none;
            color: #333;
        }}
        
        .pdf-toc a:hover {{
            color: #E91E63;
        }}
        
        /* Content sections */
        .pdf-section {{
            page-break-before: always;
            min-height: 100vh;
            padding: 40px;
        }}
        
        .pdf-section:first-of-type {{
            page-break-before: avoid;
        }}
        
        /* Hide elements */
        .md-header, .md-nav, .md-sidebar, .md-footer, 
        .md-tabs, .md-search, button {{
            display: none !important;
        }}
        
        @media print {{
            .pdf-title-page, .pdf-toc {{
                page-break-after: always;
            }}
            
            .pdf-section {{
                page-break-before: always;
            }}
            
            h1, h2, h3, h4 {{
                page-break-after: avoid;
            }}
            
            .arena-card, .admonition, pre, blockquote, table {{
                page-break-inside: avoid;
            }}
        }}
    </style>
</head>
<body>
    <main class="md-main">
        <div class="md-main__inner md-grid">
            <div class="md-content">
"""
        
        # Add title page
        from datetime import datetime
        current_date = datetime.now().strftime("%B %Y")
        
        html += f"""
                <!-- Title Page -->
                <div class="pdf-title-page">
                    <h1>Studio3 {guide_name} Guide</h1>
                    <p class="subtitle">Complete Documentation</p>
                    <p class="date">{current_date}</p>
                </div>
"""
        
        # Add table of contents
        html += """
                <!-- Table of Contents -->
                <div class="pdf-toc">
                    <h2>Table of Contents</h2>
                    <ul>
"""
        
        # Group pages by section
        current_section = None
        for page in pages:
            if page['section'] and page['section'] != current_section:
                if current_section:
                    html += "                        </ul>\n                    </li>\n"
                current_section = page['section']
                html += f'                    <li>\n                        <div class="toc-section">{current_section}</div>\n                        <ul>\n'
            
            html += f'                            <li class="toc-page"><a href="#{page["path"].replace("/", "-").replace(".md", "")}">{page["title"]}</a></li>\n'
        
        if current_section:
            html += "                        </ul>\n                    </li>\n"
        
        html += """
                    </ul>
                </div>
"""
        
        # Add all page contents
        for i, page in enumerate(pages):
            print(f"  Processing: {page['title']}...")
            content = self.fetch_page_content(page['path'])
            
            if content:
                page_id = page['path'].replace('/', '-').replace('.md', '')
                section_class = 'pdf-section' if i > 0 else 'pdf-section first-section'
                
                html += f"""
                <!-- {page['title']} -->
                <div id="{page_id}" class="{section_class}">
                    <article class="md-content__inner md-typeset">
                        {content}
                    </article>
                </div>
"""
        
        # Close HTML
        html += """
            </div>
        </div>
    </main>
</body>
</html>
"""
        
        return html
    
    def generate_pdf_wkhtmltopdf(self, html_content, output_path, guide_name):
        """Generate PDF using wkhtmltopdf"""
        
        # Save HTML to temporary file
        temp_html = Path(f'temp_{guide_name.lower()}_guide.html')
        with open(temp_html, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        # wkhtmltopdf options for high quality output
        options = [
            'wkhtmltopdf',
            '--page-size', 'A4',
            '--orientation', 'Portrait',
            '--margin-top', '25mm',
            '--margin-right', '20mm',
            '--margin-bottom', '25mm',
            '--margin-left', '20mm',
            '--encoding', 'UTF-8',
            '--enable-local-file-access',
            '--enable-javascript',
            '--javascript-delay', '2000',
            '--no-stop-slow-scripts',
            '--print-media-type',
            '--footer-center', f'Studio3 {guide_name} Guide - Page [page] of [toPage]',
            '--footer-font-size', '9',
            '--footer-spacing', '5',
            str(temp_html),
            str(output_path)
        ]
        
        try:
            subprocess.run(options, check=True, capture_output=True)
            print(f"  ✓ Generated {output_path}")
            return True
        except subprocess.CalledProcessError as e:
            print(f"  ✗ Error generating PDF: {e}")
            if e.stderr:
                print(f"    {e.stderr.decode()}")
            return False
        except FileNotFoundError:
            print("  ✗ wkhtmltopdf not found. Please install it first.")
            print("    Ubuntu/Debian: sudo apt-get install wkhtmltopdf")
            print("    macOS: brew install --cask wkhtmltopdf")
            print("    Or download from: https://wkhtmltopdf.org/downloads.html")
            return False
        finally:
            # Clean up temp file
            if temp_html.exists():
                temp_html.unlink()

def main():
    """Main function to generate all guide PDFs"""
    
    # Start MkDocs server
    print("Starting MkDocs server...")
    server = subprocess.Popen(
        ['mkdocs', 'serve', '--no-livereload'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    # Wait for server to start
    time.sleep(3)
    
    try:
        generator = PDFGenerator()
        
        # Load navigation
        nav = generator.load_navigation()
        
        # Define guides
        guides = [
            {'name': 'Overview', 'nav_key': 'Overview Guide'},
            {'name': 'Senders', 'nav_key': 'Senders Guide'},
            {'name': 'Echoes', 'nav_key': 'Echoes Guide'},
            {'name': 'Anchors', 'nav_key': 'Anchors Guide'}
        ]
        
        # Create output directories
        pdf_dir = Path('site/pdf')
        pdf_dir.mkdir(parents=True, exist_ok=True)
        
        docs_pdf_dir = Path('docs/pdf')
        docs_pdf_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate each guide
        for guide in guides:
            print(f"\nGenerating {guide['name']} Guide PDF...")
            
            # Extract pages
            pages = generator.extract_guide_pages(nav, guide['nav_key'])
            print(f"  Found {len(pages)} pages")
            
            if not pages:
                continue
            
            # Generate combined HTML
            html_content = generator.generate_combined_html(guide['name'], pages)
            
            # Generate PDF
            output_filename = f"studio3-{guide['name'].lower()}-guide.pdf"
            output_path = pdf_dir / output_filename
            
            if generator.generate_pdf_wkhtmltopdf(html_content, output_path, guide['name']):
                # Copy to docs/pdf
                import shutil
                docs_path = docs_pdf_dir / output_filename
                shutil.copy2(output_path, docs_path)
                
                # Check file size
                size_mb = output_path.stat().st_size / (1024 * 1024)
                print(f"  Size: {size_mb:.1f} MB")
        
        print("\n✅ PDF generation complete!")
        print(f"PDFs are available in: {docs_pdf_dir}")
        
    finally:
        # Stop server
        server.terminate()
        server.wait()
        print("\nMkDocs server stopped")

if __name__ == '__main__':
    main()