#!/usr/bin/env python3
"""
Fix incomplete bold markdown formatting in all .md files.
Changes patterns like **text*  to **text**
"""

import os
import re
import sys

def fix_markdown_file(filepath):
    """Fix incomplete bold markdown patterns in a file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Pattern to match **text* at end of line (with optional trailing whitespace)
    pattern = r'\*\*([^*]+)\*(\s*)$'
    replacement = r'**\1**\2'
    
    # Count replacements
    new_content, count = re.subn(pattern, replacement, content, flags=re.MULTILINE)
    
    if count > 0:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Fixed {count} patterns in {filepath}")
        return count
    return 0

def main():
    """Walk through docs directory and fix all .md files."""
    docs_dir = '/home/inocult/projects/studio3-docs/docs'
    total_fixes = 0
    files_fixed = 0
    
    for root, dirs, files in os.walk(docs_dir):
        for file in files:
            if file.endswith('.md'):
                filepath = os.path.join(root, file)
                fixes = fix_markdown_file(filepath)
                if fixes > 0:
                    total_fixes += fixes
                    files_fixed += 1
    
    print(f"\nSummary: Fixed {total_fixes} patterns across {files_fixed} files")

if __name__ == "__main__":
    main()