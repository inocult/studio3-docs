#!/usr/bin/env python3
"""
Fix all HTML headers (h1-h6) in arena-card divs to use markdown headers.
This ensures proper markdown rendering with the markdown="1" attribute.
"""

import os
import re
import sys
from pathlib import Path

def fix_html_headers_in_arena_cards(content):
    """
    Convert HTML headers to markdown headers inside arena-card divs.
    Also checks for other HTML tags that should be markdown.
    """
    lines = content.split('\n')
    in_arena_card = False
    modified = False
    result_lines = []
    
    for i, line in enumerate(lines):
        # Check if we're entering an arena-card div
        if '<div class="arena-card"' in line:
            in_arena_card = True
            # Also check if markdown="1" is present
            if 'markdown="1"' not in line:
                print(f"  Warning: arena-card div missing markdown=\"1\" attribute at line {i+1}")
        
        # Check if we're leaving the arena-card div
        elif '</div>' in line and in_arena_card:
            in_arena_card = False
        
        # If we're inside an arena-card, check for HTML tags
        elif in_arena_card:
            original_line = line
            
            # Convert h1-h6 tags to markdown headers
            for level in range(1, 7):
                # Match both complete tags like <h3>text</h3> and incomplete like <h3>text
                pattern = f'<h{level}>(.*?)(?:</h{level}>)?$'
                match = re.match(pattern, line)
                if match:
                    header_text = match.group(1).strip()
                    markdown_header = '#' * level + ' ' + header_text
                    line = markdown_header
                    modified = True
                    print(f"  Line {i+1}: Converted <h{level}> to {markdown_header}")
            
            # Check for other common HTML tags that should be markdown
            if in_arena_card and line.strip():
                # Check for bold tags
                if '<strong>' in line or '</strong>' in line:
                    line = re.sub(r'<strong>(.*?)</strong>', r'**\1**', line)
                    if line != original_line:
                        modified = True
                        print(f"  Line {i+1}: Converted <strong> to **")
                
                # Check for italic tags
                if '<em>' in line or '</em>' in line:
                    line = re.sub(r'<em>(.*?)</em>', r'*\1*', line)
                    if line != original_line:
                        modified = True
                        print(f"  Line {i+1}: Converted <em> to *")
                
                # Check for code tags
                if '<code>' in line or '</code>' in line:
                    line = re.sub(r'<code>(.*?)</code>', r'`\1`', line)
                    if line != original_line:
                        modified = True
                        print(f"  Line {i+1}: Converted <code> to `")
                
                # Check for break tags
                if '<br>' in line or '<br/>' in line or '<br />' in line:
                    line = re.sub(r'<br\s*/?>', '  ', line)  # Two spaces for line break
                    if line != original_line:
                        modified = True
                        print(f"  Line {i+1}: Converted <br> to double space")
                
                # Warn about other HTML tags
                html_tags = re.findall(r'<(?!/)([a-zA-Z]+)[^>]*>', line)
                for tag in html_tags:
                    if tag not in ['div']:  # div is expected for arena-card
                        print(f"  Warning: Found HTML <{tag}> tag at line {i+1}")
        
        result_lines.append(line)
    
    return '\n'.join(result_lines), modified

def process_file(filepath):
    """Process a single markdown file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if file has arena-card divs
        if '<div class="arena-card"' not in content:
            return False
        
        print(f"\nProcessing: {filepath}")
        
        # Fix HTML headers in arena-cards
        fixed_content, was_modified = fix_html_headers_in_arena_cards(content)
        
        if was_modified:
            # Write the fixed content back
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(fixed_content)
            print(f"  ✅ Fixed HTML headers in arena-card divs")
            return True
        else:
            print(f"  ✓ No HTML headers found in arena-card divs")
            return False
            
    except Exception as e:
        print(f"  ❌ Error processing {filepath}: {str(e)}")
        return False

def main():
    """Main function to process all markdown files."""
    docs_dir = Path('docs')
    
    if not docs_dir.exists():
        print("❌ Error: 'docs' directory not found!")
        sys.exit(1)
    
    # Find all markdown files
    md_files = list(docs_dir.rglob('*.md'))
    
    print(f"🔍 Scanning {len(md_files)} markdown files for HTML headers in arena-card divs...")
    
    modified_count = 0
    files_with_arena_cards = 0
    
    for filepath in sorted(md_files):
        if '<div class="arena-card"' in filepath.read_text(encoding='utf-8'):
            files_with_arena_cards += 1
            if process_file(filepath):
                modified_count += 1
    
    print(f"\n📊 Summary:")
    print(f"  - Total files scanned: {len(md_files)}")
    print(f"  - Files with arena-card divs: {files_with_arena_cards}")
    print(f"  - Files modified: {modified_count}")
    
    if modified_count > 0:
        print(f"\n✅ Successfully fixed {modified_count} files!")
        print("\n💡 Next steps:")
        print("  1. Review the changes with 'git diff'")
        print("  2. Run the linter to verify: python3 lint_markdown_ultra.py")
        print("  3. Test the site locally with 'mkdocs serve'")
        print("  4. Commit the changes")
    else:
        print("\n✅ No HTML headers found in arena-card divs. All files are clean!")

if __name__ == "__main__":
    main()