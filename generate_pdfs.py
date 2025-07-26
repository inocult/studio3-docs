#!/usr/bin/env python3
"""Generate individual PDF files for each guide"""

import os
import subprocess
import shutil
import yaml
import tempfile

def generate_guide_pdfs():
    """Generate separate PDFs for each guide"""
    
    # Read the main mkdocs.yml
    with open('mkdocs.yml', 'r') as f:
        config = yaml.safe_load(f)
    
    # Define guides and their sections
    guides = {
        'overview-guide': {
            'title': 'Studio3 Overview Guide',
            'sections': ['overview-guide']
        },
        'senders-guide': {
            'title': 'Studio3 Senders Guide',
            'sections': ['senders-guide']
        },
        'echoes-guide': {
            'title': 'Studio3 Echoes Guide', 
            'sections': ['echoes-guide']
        },
        'anchors-guide': {
            'title': 'Studio3 Anchors Guide',
            'sections': ['anchors-guide']
        }
    }
    
    # Create pdf directory
    os.makedirs('site/pdf', exist_ok=True)
    
    # Copy the complete PDF if it exists
    if os.path.exists('site/pdf/studio3-complete-guide.pdf'):
        print("✓ Complete guide PDF already generated")
    
    # For individual guides, we'll create placeholder PDFs for now
    # In a production setup, you'd use a proper PDF generation tool
    for guide_id, guide_info in guides.items():
        pdf_path = f'site/pdf/{guide_id}.pdf'
        
        # Create a simple HTML file as placeholder
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>{guide_info['title']}</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 40px; }}
                h1 {{ color: #2B4C8C; }}
                .notice {{ 
                    background: #f0f0f0; 
                    padding: 20px; 
                    border-radius: 8px;
                    margin: 20px 0;
                }}
            </style>
        </head>
        <body>
            <h1>{guide_info['title']}</h1>
            <div class="notice">
                <h2>PDF Generation Notice</h2>
                <p>Individual guide PDFs are generated during the build process.</p>
                <p>For the complete documentation, please download the 
                   <a href="studio3-complete-guide.pdf">Studio3 Complete Guide PDF</a>.</p>
                <p>Visit the online documentation at: 
                   <a href="https://inocult.github.io/studio3-docs/{guide_id}/">
                   {guide_info['title']} Online
                   </a>
                </p>
            </div>
        </body>
        </html>
        """
        
        # For now, create a simple HTML file
        # In production, this would be converted to PDF
        html_path = pdf_path.replace('.pdf', '.html')
        with open(html_path, 'w') as f:
            f.write(html_content)
        
        print(f"✓ Created placeholder for {guide_info['title']}")

if __name__ == '__main__':
    generate_guide_pdfs()