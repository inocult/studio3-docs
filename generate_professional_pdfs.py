#!/usr/bin/env python3
"""
Generate professional PDF files for each guide with custom styling
Uses WeasyPrint with custom CSS for Studio3 branding
"""

import os
import sys
import yaml
import re
import shutil
from pathlib import Path
from bs4 import BeautifulSoup
from weasyprint import HTML, CSS
from weasyprint.text.fonts import FontConfiguration
import markdown
from datetime import datetime
import base64

class ProfessionalPDFGenerator:
    def __init__(self):
        self.font_config = FontConfiguration()
        self.guides = {
            'overview-guide': {
                'title': 'Studio3 Overview Guide',
                'subtitle': 'Complete Platform Introduction',
                'output': 'docs/pdf/studio3-overview-guide.pdf'
            },
            'quickstart': {
                'title': 'Studio3 Quick Start Guide',
                'subtitle': 'Get Started in Minutes',
                'output': 'docs/pdf/studio3-quickstart-guide.pdf'
            },
            'senders-guide': {
                'title': 'Studio3 Senders Guide',
                'subtitle': 'Building Ventures in Public',
                'output': 'docs/pdf/studio3-senders-guide.pdf'
            },
            'echoes-guide': {
                'title': 'Studio3 Echoes Guide',
                'subtitle': 'Signal Your Conviction',
                'output': 'docs/pdf/studio3-echoes-guide.pdf'
            },
            'anchors-guide': {
                'title': 'Studio3 Anchors Guide',
                'subtitle': 'Validate and Guide Ventures',
                'output': 'docs/pdf/studio3-anchors-guide.pdf'
            }
        }
        
    def load_navigation(self):
        """Load navigation structure from mkdocs.yml"""
        with open('mkdocs.yml', 'r') as f:
            content = f.read()
        
        # Remove problematic tags
        content = re.sub(r'!!python/name:[^\s]+', '{}', content)
        
        config = yaml.safe_load(content)
        return config.get('nav', [])
    
    def extract_guide_pages(self, nav, guide_key):
        """Extract all pages for a specific guide"""
        pages = []
        
        # Map guide keys to navigation titles
        guide_map = {
            'overview-guide': 'Overview Guide',
            'quickstart': 'Quickstart',
            'senders-guide': 'Senders Guide',
            'echoes-guide': 'Echoes Guide',
            'anchors-guide': 'Anchors Guide'
        }
        
        target_title = guide_map.get(guide_key)
        if not target_title:
            return pages
        
        def process_item(item, level=0, in_target=False):
            if isinstance(item, dict):
                for title, value in item.items():
                    # Check if this is our target guide
                    is_target_guide = (title == target_title and level == 0)
                    current_in_target = in_target or is_target_guide
                    
                    if current_in_target:
                        if isinstance(value, str):
                            # This is a page - add it
                            pages.append({
                                'title': title,
                                'path': value,
                                'level': level
                            })
                        elif isinstance(value, list):
                            # This is a section
                            if level > 0:  # Don't add the main guide title as section
                                pages.append({
                                    'title': title,
                                    'path': None,
                                    'level': level
                                })
                            # Process sub-items
                            for sub_item in value:
                                process_item(sub_item, level + 1, current_in_target)
                    elif isinstance(value, list) and not in_target:
                        # Keep looking for our guide
                        for sub_item in value:
                            process_item(sub_item, level, False)
        
        # Process each top-level navigation item
        for item in nav:
            process_item(item, 0, False)
            
        return pages
    
    def get_logo_base64(self):
        """Convert logo to base64 for embedding"""
        logo_path = Path('Studio3.png')
        if logo_path.exists():
            with open(logo_path, 'rb') as f:
                logo_data = f.read()
            return base64.b64encode(logo_data).decode('utf-8')
        return None
    
    def create_cover_page(self, guide_info):
        """Create a professional cover page"""
        logo_base64 = self.get_logo_base64()
        logo_tag = f'<img src="data:image/png;base64,{logo_base64}" alt="Studio3 Logo" class="logo">' if logo_base64 else ''
        
        return f"""
        <div class="cover-page">
            <div class="cover-content">
                {logo_tag}
                <h1 class="cover-title">{guide_info['title']}</h1>
                <h2 class="cover-subtitle">{guide_info['subtitle']}</h2>
                <div class="cover-meta">
                    <p>Version 1.0</p>
                    <p>{datetime.now().strftime('%B %Y')}</p>
                </div>
            </div>
            <div class="cover-footer">
                <p>Where belief becomes momentum</p>
            </div>
        </div>
        """
    
    def create_toc_page(self, pages):
        """Create table of contents page"""
        toc_html = '<div class="toc-page"><h1>Table of Contents</h1><div class="toc-content">'
        
        current_section = None
        for page in pages:
            if page['path'] is None:
                # Section header
                if current_section:
                    toc_html += '</div>'
                toc_html += f'<div class="toc-section"><h2>{page["title"]}</h2>'
                current_section = page['title']
            else:
                # Regular page
                indent_class = f'toc-level-{page["level"]}'
                toc_html += f'<div class="toc-item {indent_class}">'
                toc_html += f'<span class="toc-title">{page["title"]}</span>'
                toc_html += f'<span class="toc-dots"></span>'
                toc_html += f'<span class="toc-page-num" data-page="{page["path"]}"></span>'
                toc_html += '</div>'
        
        if current_section:
            toc_html += '</div>'
        
        toc_html += '</div></div>'
        return toc_html
    
    def process_markdown_content(self, content):
        """Process markdown content with extensions"""
        # Remove image references that won't work in PDF
        content = re.sub(r'!\[[^\]]*\]\([^)]+\)', '[Image]', content)
        
        md = markdown.Markdown(extensions=[
            'extra',
            'codehilite',
            'tables',
            'toc',
            'admonition',
            'pymdownx.superfences',
            'pymdownx.details',
            'pymdownx.tabbed',
            'attr_list',
            'md_in_html'
        ])
        
        # Pre-process arena-card divs
        content = re.sub(
            r'<div class="arena-card"[^>]*>\s*',
            r'<div class="arena-card">',
            content
        )
        
        html = md.convert(content)
        
        # Post-process for better PDF rendering
        soup = BeautifulSoup(html, 'html.parser')
        
        # Process arena cards
        for card in soup.find_all('div', class_='arena-card'):
            card['class'] = ['arena-card', 'pdf-arena-card']
        
        # Fix tables
        for table in soup.find_all('table'):
            table['class'] = table.get('class', []) + ['pdf-table']
        
        # Process admonitions
        for admonition in soup.find_all('div', class_='admonition'):
            admonition['class'] = admonition.get('class', []) + ['pdf-admonition']
        
        return str(soup)
    
    def get_custom_css(self):
        """Generate comprehensive custom CSS for PDF"""
        return """
        @page {
            size: A4;
            margin: 2.5cm 2cm 2.5cm 2cm;
            @bottom-center {
                content: counter(page) " / " counter(pages);
                font-size: 10pt;
                color: #666;
            }
            @top-left {
                content: string(chapter-title);
                font-size: 9pt;
                color: #666;
                font-style: italic;
            }
            @top-right {
                content: "Studio3 Documentation";
                font-size: 9pt;
                color: #666;
            }
        }
        
        @page:first {
            @top-left { content: none; }
            @top-right { content: none; }
            @bottom-center { content: none; }
        }
        
        /* Base styles */
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            font-size: 11pt;
            line-height: 1.6;
            color: #333;
            text-align: justify;
            hyphens: auto;
        }
        
        /* Cover page */
        .cover-page {
            page-break-after: always;
            height: 100vh;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            text-align: center;
            padding: 0;
        }
        
        .cover-content {
            flex-grow: 1;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
        }
        
        .cover-page .logo {
            width: 200px;
            height: auto;
            margin-bottom: 3cm;
        }
        
        .cover-title {
            font-size: 36pt;
            font-weight: 700;
            color: #1a1a1a;
            margin: 0 0 0.5cm 0;
            letter-spacing: -1px;
        }
        
        .cover-subtitle {
            font-size: 18pt;
            font-weight: 400;
            color: #666;
            margin: 0 0 2cm 0;
        }
        
        .cover-meta {
            font-size: 12pt;
            color: #888;
        }
        
        .cover-meta p {
            margin: 0.2cm 0;
        }
        
        .cover-footer {
            padding: 1cm;
            font-style: italic;
            color: #888;
            font-size: 10pt;
        }
        
        /* Table of contents */
        .toc-page {
            page-break-after: always;
        }
        
        .toc-page h1 {
            font-size: 24pt;
            margin-bottom: 1cm;
            color: #1a1a1a;
        }
        
        .toc-section {
            margin-bottom: 0.8cm;
        }
        
        .toc-section h2 {
            font-size: 14pt;
            color: #333;
            margin: 0.5cm 0 0.3cm 0;
            font-weight: 600;
        }
        
        .toc-item {
            display: flex;
            align-items: baseline;
            margin: 0.2cm 0;
            font-size: 11pt;
        }
        
        .toc-level-1 { margin-left: 0.5cm; }
        .toc-level-2 { margin-left: 1cm; }
        
        .toc-title {
            flex-shrink: 0;
        }
        
        .toc-dots {
            flex-grow: 1;
            border-bottom: 1px dotted #ccc;
            margin: 0 0.3cm;
            height: 0.8em;
        }
        
        .toc-page-num::after {
            content: attr(data-page-num);
        }
        
        /* Headers */
        h1 {
            font-size: 24pt;
            font-weight: 700;
            color: #1a1a1a;
            margin: 1cm 0 0.5cm 0;
            page-break-after: avoid;
            string-set: chapter-title content();
        }
        
        h2 {
            font-size: 18pt;
            font-weight: 600;
            color: #333;
            margin: 0.8cm 0 0.4cm 0;
            page-break-after: avoid;
        }
        
        h3 {
            font-size: 14pt;
            font-weight: 600;
            color: #444;
            margin: 0.6cm 0 0.3cm 0;
            page-break-after: avoid;
        }
        
        h4 {
            font-size: 12pt;
            font-weight: 600;
            color: #555;
            margin: 0.5cm 0 0.3cm 0;
            page-break-after: avoid;
        }
        
        /* Paragraphs and lists */
        p {
            margin: 0.3cm 0;
            orphans: 3;
            widows: 3;
        }
        
        ul, ol {
            margin: 0.3cm 0 0.3cm 0.5cm;
            padding-left: 0.5cm;
        }
        
        li {
            margin: 0.15cm 0;
            page-break-inside: avoid;
        }
        
        /* Code blocks */
        pre {
            background-color: #f8f9fa;
            border: 1px solid #e9ecef;
            border-radius: 4px;
            padding: 0.3cm;
            font-size: 9pt;
            overflow-x: auto;
            page-break-inside: avoid;
            margin: 0.4cm 0;
        }
        
        code {
            font-family: "SF Mono", Monaco, Consolas, monospace;
            font-size: 9pt;
            background-color: #f8f9fa;
            padding: 0.05cm 0.1cm;
            border-radius: 2px;
        }
        
        pre code {
            background: none;
            padding: 0;
        }
        
        /* Tables */
        .pdf-table {
            width: 100%;
            border-collapse: collapse;
            margin: 0.5cm 0;
            page-break-inside: avoid;
            font-size: 10pt;
        }
        
        .pdf-table th {
            background-color: #f8f9fa;
            font-weight: 600;
            text-align: left;
            padding: 0.3cm;
            border: 1px solid #dee2e6;
        }
        
        .pdf-table td {
            padding: 0.25cm;
            border: 1px solid #dee2e6;
        }
        
        /* Arena cards */
        .pdf-arena-card {
            background-color: #f8f9fa;
            border: 2px solid #FFE4B5;
            border-radius: 8px;
            padding: 0.5cm;
            margin: 0.5cm 0;
            page-break-inside: avoid;
        }
        
        .pdf-arena-card h3,
        .pdf-arena-card h4 {
            color: #FF6B6B;
            margin-top: 0;
        }
        
        /* Admonitions */
        .pdf-admonition {
            border-left: 4px solid #448aff;
            padding: 0.3cm 0.3cm 0.3cm 0.5cm;
            margin: 0.5cm 0;
            page-break-inside: avoid;
            background-color: #f8f9fa;
        }
        
        .pdf-admonition.warning {
            border-left-color: #ff9800;
            background-color: #fff8e1;
        }
        
        .pdf-admonition.tip {
            border-left-color: #4caf50;
            background-color: #f1f8e9;
        }
        
        .pdf-admonition.note {
            border-left-color: #2196f3;
            background-color: #e3f2fd;
        }
        
        .pdf-admonition .admonition-title {
            font-weight: 600;
            margin-bottom: 0.2cm;
        }
        
        /* Blockquotes */
        blockquote {
            border-left: 4px solid #ccc;
            padding-left: 0.5cm;
            margin: 0.4cm 0;
            font-style: italic;
            color: #666;
        }
        
        /* Links */
        a {
            color: #FF6B6B;
            text-decoration: none;
        }
        
        /* Page breaks */
        .page-break {
            page-break-after: always;
        }
        
        h1 {
            page-break-before: always;
        }
        
        .toc-page + * h1:first-child,
        .cover-page + * h1:first-child {
            page-break-before: avoid;
        }
        
        /* Emoji support */
        .emoji {
            font-family: "Apple Color Emoji", "Segoe UI Emoji", sans-serif;
        }
        """
    
    def generate_guide_pdf(self, guide_key, guide_info):
        """Generate PDF for a specific guide"""
        print(f"\n📚 Generating PDF for {guide_info['title']}...")
        
        # Load navigation and extract pages
        nav = self.load_navigation()
        pages = self.extract_guide_pages(nav, guide_key)
        
        if not pages:
            print(f"  ⚠️  No pages found for {guide_key}")
            return False
        
        # Create HTML content
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>{guide_info['title']}</title>
        </head>
        <body>
        """
        
        # Add cover page
        html_content += self.create_cover_page(guide_info)
        
        # Add table of contents
        html_content += self.create_toc_page(pages)
        
        # Add content pages
        page_num = 3  # After cover and TOC
        for page in pages:
            if page['path'] is None:
                # Section divider
                html_content += f'<h1 class="section-header">{page["title"]}</h1>'
            else:
                # Read and process markdown file
                file_path = Path('docs') / page['path']
                if file_path.exists():
                    print(f"  📄 Processing {page['path']}...")
                    
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Process markdown to HTML
                    page_html = self.process_markdown_content(content)
                    
                    # Add to document
                    html_content += f'<div class="content-page" data-page-num="{page_num}">'
                    html_content += f'<h1>{page["title"]}</h1>'
                    html_content += page_html
                    html_content += '</div>'
                    
                    page_num += 1
                else:
                    print(f"  ⚠️  File not found: {file_path}")
        
        html_content += """
        </body>
        </html>
        """
        
        # Generate PDF with WeasyPrint
        try:
            # Ensure output directory exists
            output_path = Path(guide_info['output'])
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Create PDF
            css = CSS(string=self.get_custom_css(), font_config=self.font_config)
            HTML(string=html_content).write_pdf(
                output_path,
                stylesheets=[css],
                font_config=self.font_config
            )
            
            print(f"  ✅ PDF generated: {output_path}")
            return True
            
        except Exception as e:
            print(f"  ❌ Error generating PDF: {e}")
            return False
    
    def generate_all_pdfs(self):
        """Generate PDFs for all guides"""
        print("🚀 Starting professional PDF generation...")
        
        success_count = 0
        for guide_key, guide_info in self.guides.items():
            if self.generate_guide_pdf(guide_key, guide_info):
                success_count += 1
        
        print(f"\n✨ PDF generation complete! {success_count}/{len(self.guides)} guides processed.")
        
        return success_count == len(self.guides)

def main():
    """Main entry point"""
    generator = ProfessionalPDFGenerator()
    success = generator.generate_all_pdfs()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()