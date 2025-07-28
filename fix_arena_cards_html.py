#!/usr/bin/env python3
"""
Script to convert arena-cards with nested HTML to pure HTML format
"""

import os
import re
import glob
from pathlib import Path

def convert_arena_card_to_html(content):
    """Convert arena-cards that contain HTML to pure HTML format"""
    
    lines = content.split('\n')
    result_lines = []
    i = 0
    
    while i < len(lines):
        line = lines[i]
        
        # Check for arena-card start with markdown="1"
        if '<div class="arena-card" markdown="1">' in line:
            # Found arena-card start, collect all content until </div>
            arena_content = []
            i += 1  # Skip the opening div
            
            # Collect content until we find the closing </div>
            div_depth = 1
            has_nested_html = False
            
            while i < len(lines) and div_depth > 0:
                current_line = lines[i]
                
                # Check for nested HTML elements
                if re.search(r'<[^>]+>', current_line) and not current_line.strip().startswith('```'):
                    has_nested_html = True
                
                # Track div depth
                if '<div' in current_line:
                    div_depth += 1
                elif '</div>' in current_line:
                    div_depth -= 1
                
                if div_depth > 0:  # Don't include the closing </div>
                    arena_content.append(current_line)
                
                i += 1
            
            # If this arena-card has nested HTML, convert to pure HTML
            if has_nested_html:
                # Remove markdown="1" from opening tag
                result_lines.append('<div class="arena-card">')
                
                # Convert markdown content to HTML
                converted_content = convert_markdown_to_html(arena_content)
                result_lines.extend(converted_content)
                
                # Add closing div
                result_lines.append('</div>')
            else:
                # Keep as markdown arena-card
                result_lines.append('<div class="arena-card" markdown="1">')
                result_lines.extend(arena_content)
                result_lines.append('</div>')
        else:
            result_lines.append(line)
            i += 1
    
    return '\n'.join(result_lines)

def convert_markdown_to_html(lines):
    """Convert common markdown elements to HTML"""
    
    result = []
    in_list = False
    
    for line in lines:
        stripped = line.strip()
        indent = len(line) - len(line.lstrip())
        
        if not stripped:
            result.append('')
            continue
        
        # Convert headers
        if stripped.startswith('### '):
            result.append(f'<h3>{stripped[4:]}</h3>')
        elif stripped.startswith('## '):
            result.append(f'<h2>{stripped[3:]}</h2>')
        elif stripped.startswith('# '):
            result.append(f'<h1>{stripped[2:]}</h1>')
        
        # Convert lists
        elif stripped.startswith('- ') or stripped.startswith('* '):
            if not in_list:
                result.append('<ul>')
                in_list = True
            list_content = stripped[2:]
            result.append(f'<li>{list_content}</li>')
        
        # Regular paragraph text
        elif not stripped.startswith('<') and not stripped.startswith('```'):
            if in_list:
                result.append('</ul>')
                in_list = False
            result.append(f'<p>{stripped}</p>')
        
        # Keep HTML as-is
        else:
            if in_list and not stripped.startswith('<li') and stripped.startswith('<'):
                result.append('</ul>')
                in_list = False
            result.append(line)
    
    # Close any open lists
    if in_list:
        result.append('</ul>')
    
    return result

def fix_file(filepath):
    """Fix arena-cards in a single file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            original_content = f.read()
        
        # Only process files that have arena-cards with markdown="1"
        if 'arena-card" markdown="1"' not in original_content:
            return False
        
        fixed_content = convert_arena_card_to_html(original_content)
        
        if fixed_content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(fixed_content)
            print(f"Fixed: {filepath}")
            return True
        else:
            print(f"No changes: {filepath}")
            return False
            
    except Exception as e:
        print(f"Error processing {filepath}: {str(e)}")
        return False

def main():
    """Fix arena-cards in all markdown files"""
    docs_dir = 'docs'
    md_files = glob.glob(os.path.join(docs_dir, '**/*.md'), recursive=True)
    
    print(f"Processing {len(md_files)} markdown files for arena-card HTML conversion...")
    
    fixed_count = 0
    for filepath in sorted(md_files):
        if fix_file(filepath):
            fixed_count += 1
    
    print(f"\nCompleted: {fixed_count} files modified")

if __name__ == "__main__":
    main()