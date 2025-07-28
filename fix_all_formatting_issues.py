#!/usr/bin/env python3
"""Fix common formatting issues across all markdown files."""

import re
import os
from pathlib import Path
import glob

def fix_formatting_issues(file_path):
    """Fix common formatting issues in a markdown file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        lines = content.split('\n')
    
    fixed_lines = []
    in_code_block = False
    in_arena_card = False
    i = 0
    
    while i < len(lines):
        line = lines[i]
        
        # Track code blocks
        if line.strip().startswith('```'):
            in_code_block = not in_code_block
            fixed_lines.append(line)
            i += 1
            continue
            
        # Track arena-card divs
        if '<div class="arena-card"' in line:
            in_arena_card = True
        elif '</div>' in line and in_arena_card:
            in_arena_card = False
        
        # Skip formatting in code blocks
        if in_code_block:
            fixed_lines.append(line)
            i += 1
            continue
        
        # Fix multiple consecutive spaces (but not in code blocks or at line start)
        if not line.startswith('    ') and not line.startswith('\t'):
            # Replace multiple spaces with single space, but preserve indentation
            indent_match = re.match(r'^(\s*)', line)
            if indent_match:
                indent = indent_match.group(1)
                rest_of_line = line[len(indent):]
                # Fix multiple spaces in the non-indent part
                rest_of_line = re.sub(r'(?<!^)\s{2,}', ' ', rest_of_line)
                line = indent + rest_of_line
        
        # Fix space after/before bold markers
        line = re.sub(r'\*\*\s+', '**', line)  # Remove space after **
        line = re.sub(r'\s+\*\*', '**', line)  # Remove space before **
        
        # Fix missing space after colon (but not in URLs or time formats)
        line = re.sub(r'(?<!http)(?<!https)(?<!\d):(?![/\d])(?!\s)', ': ', line)
        
        # Fix unclosed bold markers - if line has odd number of **
        star_count = line.count('**')
        if star_count % 2 == 1:
            # Try to fix by adding ** at the end if it makes sense
            if line.strip() and not line.strip().endswith('**'):
                line = line.rstrip() + '**'
        
        # Fix bold header with colon needing blank line before list
        if re.match(r'^\*\*[^*]+\*\*:\s*$', line.strip()):
            # Check if next non-empty line is a list
            next_idx = i + 1
            while next_idx < len(lines) and not lines[next_idx].strip():
                next_idx += 1
            
            if next_idx < len(lines):
                next_line = lines[next_idx].strip()
                if re.match(r'^[-*\d]', next_line) or re.match(r'^\d+\.', next_line):
                    # Ensure exactly one blank line
                    fixed_lines.append(line)
                    fixed_lines.append('')  # Add blank line
                    i = next_idx  # Skip to the list line
                    continue
        
        fixed_lines.append(line)
        i += 1
    
    return '\n'.join(fixed_lines)

def fix_grid_divs(content):
    """Fix grid divs missing markdown='1' attribute."""
    # Pattern to find grid divs without markdown='1'
    pattern = r'<div class="grid"(?![^>]*markdown=)([^>]*)>'
    replacement = r'<div class="grid" markdown="1"\1>'
    return re.sub(pattern, replacement, content)

def process_file(file_path):
    """Process a single file and return the number of changes made."""
    print(f"Processing: {file_path}")
    
    original_content = open(file_path, 'r', encoding='utf-8').read()
    
    # First fix general formatting issues
    fixed_content = fix_formatting_issues(file_path)
    
    # Then fix grid divs
    fixed_content = fix_grid_divs(fixed_content)
    
    if original_content != fixed_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(fixed_content)
        print(f"  ✓ Fixed formatting issues")
        return 1
    else:
        print(f"  - No changes needed")
        return 0

def main():
    """Fix formatting issues in all markdown files."""
    # Find all markdown files in docs directory
    md_files = glob.glob('docs/**/*.md', recursive=True)
    
    # Sort by path for better output
    md_files.sort()
    
    total_fixed = 0
    
    for file_path in md_files:
        if os.path.exists(file_path):
            total_fixed += process_file(file_path)
    
    print(f"\nTotal files fixed: {total_fixed}")
    print(f"Total files processed: {len(md_files)}")

if __name__ == "__main__":
    main()