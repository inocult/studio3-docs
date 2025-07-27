#!/usr/bin/env python3
import os
import re

def fix_info_blocks(content):
    """Fix info block formatting where bold text with colons is split across lines."""
    # Pattern to match info blocks
    lines = content.split('\n')
    fixed_lines = []
    i = 0
    
    while i < len(lines):
        line = lines[i]
        
        # Check if we're in an info block
        if line.strip().startswith('!!! info') or line.strip().startswith('!!! warning') or line.strip().startswith('!!! tip'):
            fixed_lines.append(line)
            i += 1
            
            # Process the content of the info block
            while i < len(lines) and not lines[i].strip().startswith('!!!'):
                current_line = lines[i]
                
                # Check if this line starts with spaces and contains **text:
                if '    **' in current_line and current_line.strip().endswith(':'):
                    # This is the start of a broken bold text with colon
                    bold_text = current_line
                    i += 1
                    
                    # Skip empty line if present
                    if i < len(lines) and lines[i].strip() == '':
                        i += 1
                    
                    # Get the continuation (should end with **)
                    if i < len(lines) and lines[i].strip().endswith('**'):
                        continuation = lines[i].strip()
                        # Combine them on one line
                        fixed_line = bold_text.rstrip(':') + ':' + continuation
                        fixed_lines.append(fixed_line)
                        i += 1
                    else:
                        # If no continuation found, just add the original line
                        fixed_lines.append(current_line)
                        i += 1
                else:
                    fixed_lines.append(current_line)
                    i += 1
        else:
            fixed_lines.append(line)
            i += 1
    
    return '\n'.join(fixed_lines)

def process_file(filepath):
    """Process a single file to fix formatting."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    fixed_content = fix_info_blocks(content)
    
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