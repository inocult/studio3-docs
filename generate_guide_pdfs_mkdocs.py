#!/usr/bin/env python3
"""Generate individual guide PDFs using mkdocs-pdf-export plugin"""

import os
import shutil
import subprocess
import yaml
import re
from pathlib import Path

def create_guide_config(guide_name, guide_pages, base_config):
    """Create a temporary mkdocs.yml for a specific guide"""
    
    config = base_config.copy()
    
    # Update site name
    config['site_name'] = f"Studio3 {guide_name} Guide"
    
    # Set navigation to only include this guide
    config['nav'] = [{f"{guide_name} Guide": guide_pages}]
    
    # Update PDF export settings
    if 'plugins' not in config:
        config['plugins'] = []
    
    # Find and update pdf-export plugin settings
    for i, plugin in enumerate(config['plugins']):
        if isinstance(plugin, dict) and 'pdf-export' in plugin:
            plugin['pdf-export']['combined'] = True
            plugin['pdf-export']['combined_output_path'] = f"pdf/studio3-{guide_name.lower()}-guide.pdf"
            config['plugins'][i] = plugin
            break
    
    # Add enhanced PDF stylesheet
    if 'extra_css' not in config:
        config['extra_css'] = []
    if 'stylesheets/pdf-enhanced.css' not in config['extra_css']:
        config['extra_css'].append('stylesheets/pdf-enhanced.css')
    
    return config

def load_base_config():
    """Load and clean the base mkdocs.yml configuration"""
    with open('mkdocs.yml', 'r') as f:
        content = f.read()
    
    # Remove problematic Python object tags
    content = re.sub(r'!!python/name:[^\s]+', '{}', content)
    
    return yaml.safe_load(content)

def extract_guide_from_nav(nav, guide_key):
    """Extract a specific guide's pages from the navigation"""
    for item in nav:
        if isinstance(item, dict):
            for key, value in item.items():
                if guide_key in key:
                    return value
    return None

def main():
    """Generate individual PDFs for each guide"""
    
    print("Loading base configuration...")
    base_config = load_base_config()
    
    # Define guides to generate
    guides = [
        {
            'name': 'Overview',
            'nav_key': 'Overview Guide',
            'filename': 'overview'
        },
        {
            'name': 'Senders',
            'nav_key': 'Senders Guide',
            'filename': 'senders'
        },
        {
            'name': 'Echoes',
            'nav_key': 'Echoes Guide',
            'filename': 'echoes'
        },
        {
            'name': 'Anchors',
            'nav_key': 'Anchors Guide',
            'filename': 'anchors'
        }
    ]
    
    # Create output directories
    output_dir = Path('generated_pdfs')
    output_dir.mkdir(exist_ok=True)
    
    docs_pdf_dir = Path('docs/pdf')
    docs_pdf_dir.mkdir(parents=True, exist_ok=True)
    
    # Set environment variable to enable PDF export
    os.environ['ENABLE_PDF_EXPORT'] = '1'
    
    for guide in guides:
        print(f"\n{'='*60}")
        print(f"Generating PDF for {guide['name']} Guide...")
        print('='*60)
        
        # Extract guide pages from navigation
        guide_pages = extract_guide_from_nav(base_config['nav'], guide['nav_key'])
        
        if not guide_pages:
            print(f"Warning: Could not find {guide['nav_key']} in navigation")
            continue
        
        # Create temporary config for this guide
        guide_config = create_guide_config(guide['name'], guide_pages, base_config)
        
        # Write temporary config
        temp_config = Path(f'mkdocs_{guide["filename"]}.yml')
        with open(temp_config, 'w') as f:
            yaml.dump(guide_config, f, default_flow_style=False, sort_keys=False)
        
        try:
            # Build the site with PDF export for this guide
            print(f"Building {guide['name']} Guide...")
            result = subprocess.run(
                ['mkdocs', 'build', '-f', str(temp_config), '--clean'],
                capture_output=True,
                text=True,
                check=True
            )
            
            # Find the generated PDF
            pdf_path = Path('site/pdf') / f"studio3-{guide['filename']}-guide.pdf"
            
            if pdf_path.exists():
                # Copy to output directory
                output_path = output_dir / f"studio3-{guide['filename']}-guide.pdf"
                shutil.copy2(pdf_path, output_path)
                
                # Also copy to docs/pdf
                docs_path = docs_pdf_dir / f"studio3-{guide['filename']}-guide.pdf"
                shutil.copy2(pdf_path, docs_path)
                
                # Check file size
                size_mb = output_path.stat().st_size / (1024 * 1024)
                print(f"✓ Generated {output_path.name} ({size_mb:.1f} MB)")
            else:
                print(f"✗ PDF not found at {pdf_path}")
                
        except subprocess.CalledProcessError as e:
            print(f"✗ Error building {guide['name']} Guide:")
            print(e.stderr)
            
        finally:
            # Clean up temporary config
            if temp_config.exists():
                temp_config.unlink()
    
    print(f"\n{'='*60}")
    print("PDF Generation Complete!")
    print(f"Generated PDFs are in: {output_dir}")
    print(f"Documentation PDFs are in: {docs_pdf_dir}")
    
    # Create an index of PDFs
    index_content = """# Studio3 Documentation PDFs

High-quality PDF versions of all Studio3 guides.

## Available Guides

"""
    
    for guide in guides:
        pdf_path = docs_pdf_dir / f"studio3-{guide['filename']}-guide.pdf"
        if pdf_path.exists():
            size_mb = pdf_path.stat().st_size / (1024 * 1024)
            index_content += f"- [{guide['name']} Guide](studio3-{guide['filename']}-guide.pdf) - {size_mb:.1f} MB\n"
    
    index_content += """
## Features

- Complete content from all guide sections
- Professional formatting and typography
- Syntax-highlighted code blocks
- Preserved Studio3 branding and colors
- Optimized for printing and digital reading
- Clickable table of contents
- Page numbers and guide identification

Generated with MkDocs PDF Export Plugin.
"""
    
    with open(docs_pdf_dir / 'index.md', 'w') as f:
        f.write(index_content)
    
    print(f"\nIndex created at: {docs_pdf_dir / 'index.md'}")

if __name__ == '__main__':
    main()