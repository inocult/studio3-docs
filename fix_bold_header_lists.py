#!/usr/bin/env python3
"""
Fix bold headers with colons that need blank lines before lists.
"""

import os
import re
import sys
from pathlib import Path

def fix_bold_header_lists(content):
    """
    Add blank lines after bold headers ending with colon before lists.
    """
    lines = content.split('\n')
    result_lines = []
    modified = False
    
    for i in range(len(lines)):
        result_lines.append(lines[i])
        
        # Check if this line is a bold header ending with colon
        if re.match(r'^\*\*[^*]+:\*\*\s*$', lines[i]):
            # Check if next line exists and is a list
            if i + 1 < len(lines):
                next_line = lines[i + 1]
                # If next line is a list item without blank line
                if (re.match(r'^[-*\d]\s+', next_line) or 
                    re.match(r'^\d+\.\s+', next_line) or
                    re.match(r'^[A-Za-z]', next_line)):  # Also catch lines that start with text
                    # Add blank line
                    result_lines.append('')
                    modified = True
                    print(f"  Line {i+1}: Added blank line after '{lines[i]}'")
    
    return '\n'.join(result_lines), modified

def process_file(filepath):
    """Process a single markdown file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        fixed_content, was_modified = fix_bold_header_lists(content)
        
        if was_modified:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(fixed_content)
            return True
        return False
            
    except Exception as e:
        print(f"  ❌ Error processing {filepath}: {str(e)}")
        return False

def main():
    """Process specific file or all files."""
    if len(sys.argv) > 1:
        # Process specific file
        filepath = sys.argv[1]
        print(f"Processing: {filepath}")
        if process_file(filepath):
            print("✅ Fixed bold header list formatting")
        else:
            print("✓ No issues found")
    else:
        # Process all markdown files
        docs_dir = Path('docs')
        md_files = list(docs_dir.rglob('*.md'))
        
        modified_count = 0
        for filepath in sorted(md_files):
            if process_file(filepath):
                print(f"Fixed: {filepath}")
                modified_count += 1
        
        print(f"\n✅ Fixed {modified_count} files")

if __name__ == "__main__":
    main()