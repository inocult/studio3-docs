#!/usr/bin/env python3
"""
Fix list formatting issues in markdown files.
Ensures bold headers with colons have blank lines before lists.
"""

import os
import re
import sys
from pathlib import Path

def fix_list_formatting(content):
    """
    Fix formatting issues with lists after bold headers.
    """
    lines = content.split('\n')
    result_lines = []
    i = 0
    modified = False
    
    while i < len(lines):
        current_line = lines[i]
        result_lines.append(current_line)
        
        # Check if this is a bold header ending with colon
        if re.match(r'^\*\*[^*]+\*\*:\s*$', current_line):
            # Look ahead to see if next line is a list
            if i + 1 < len(lines):
                next_line = lines[i + 1]
                # If next line is immediately a list item (no blank line)
                if re.match(r'^[-*\d]\s+', next_line.strip()) or re.match(r'^\d+\.\s+', next_line.strip()):
                    # Add a blank line
                    result_lines.append('')
                    modified = True
                    print(f"  Added blank line after line {i+1}: {current_line}")
        
        # Also check for missing blank lines between sections
        if i + 1 < len(lines):
            current = lines[i].strip()
            next_line = lines[i + 1].strip()
            
            # If current line ends a list/paragraph and next is a bold header
            if current and not current.startswith('#') and re.match(r'^\*\*[^*]+\*\*', next_line):
                # Check if it's not already followed by a blank line
                if current_line.strip() and lines[i + 1].strip():
                    result_lines.append('')
                    modified = True
                    print(f"  Added blank line between sections at line {i+1}")
        
        i += 1
    
    return '\n'.join(result_lines), modified

def process_file(filepath):
    """Process a single markdown file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print(f"\nProcessing: {filepath}")
        
        # Fix list formatting
        fixed_content, was_modified = fix_list_formatting(content)
        
        if was_modified:
            # Write the fixed content back
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(fixed_content)
            print(f"  ✅ Fixed list formatting issues")
            return True
        else:
            print(f"  ✓ No list formatting issues found")
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
    
    print(f"🔍 Scanning {len(md_files)} markdown files for list formatting issues...")
    
    modified_count = 0
    
    for filepath in sorted(md_files):
        if process_file(filepath):
            modified_count += 1
    
    print(f"\n📊 Summary:")
    print(f"  - Total files scanned: {len(md_files)}")
    print(f"  - Files modified: {modified_count}")
    
    if modified_count > 0:
        print(f"\n✅ Successfully fixed {modified_count} files!")
    else:
        print("\n✅ No list formatting issues found!")

if __name__ == "__main__":
    main()