#!/usr/bin/env python3
import os
import re

def fix_arena_list_spacing(content):
    """Fix list spacing issues in arena cards."""
    lines = content.split('\n')
    fixed_lines = []
    i = 0
    
    while i < len(lines):
        line = lines[i]
        fixed_lines.append(line)
        
        # Check if current line ends with ** (end of bold text) or ends with :
        # and next line starts with - (list item)
        if i + 1 < len(lines):
            current_line = line.strip()
            next_line = lines[i + 1].strip()
            
            # Check if we're inside an arena-card
            in_arena = False
            for j in range(max(0, i - 20), i):
                if j < len(lines) and 'arena-card' in lines[j]:
                    in_arena = True
                    break
            
            if in_arena:
                # If current line ends with ** or : and next line is a list item
                if ((current_line.endswith('**') or current_line.endswith(':')) and 
                    next_line.startswith(('-', '*', '1.', '2.', '3.', '4.', '5.', '6.', '7.', '8.', '9.'))):
                    # Check if there's already a blank line
                    if i + 1 < len(lines) and lines[i + 1].strip() != '':
                        fixed_lines.append('')  # Add blank line
        
        i += 1
    
    return '\n'.join(fixed_lines)

def process_file(filepath):
    """Process a single file to fix formatting."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Only process if file contains arena-card
    if 'arena-card' not in content:
        return False
    
    original_content = content
    fixed_content = fix_arena_list_spacing(content)
    
    if fixed_content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(fixed_content)
        return True
    return False

def main():
    docs_dir = '/home/inocult/projects/studio3-docs/docs'
    fixed_files = []
    
    for root, dirs, files in os.walk(docs_dir):
        for file in files:
            if file.endswith('.md'):
                filepath = os.path.join(root, file)
                if process_file(filepath):
                    fixed_files.append(filepath)
                    print(f"Fixed: {filepath}")
    
    print(f"\nTotal files fixed: {len(fixed_files)}")

if __name__ == "__main__":
    main()