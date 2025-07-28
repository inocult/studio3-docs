#!/usr/bin/env python3

import os
import re
import glob

def fix_markdown_issues(content):
    """Fix comprehensive markdown rendering issues"""
    
    # Fix broken numbered lists with double asterisks
    # Pattern: **2. **Create -> 2. **Create**
    content = re.sub(r'\*\*(\d+)\.\s+\*\*([^*\n]+)', r'\1. **\2**', content)
    
    # Fix incomplete bold patterns
    # Pattern: **text* -> **text**
    content = re.sub(r'\*\*([^*\n]+)\*(\s)', r'**\1**\2', content)
    
    # Fix lines with only bold asterisks
    content = re.sub(r'^\*\*(\d+)\.\s+\*\*(.+)$', r'\1. **\2**', content, flags=re.MULTILINE)
    
    # Fix incomplete patterns like "- Merit beats connections** "
    content = re.sub(r'([^*])\*\*(\s)', r'\1\2', content)
    
    # Fix broken bullet points with extra formatting
    # Pattern: - **text** - **text**  -> separate lines
    content = re.sub(r'^(- .+?)\s+(-\s+.+)$', r'\1\n\2', content, flags=re.MULTILINE)
    
    # Fix mixed list formatting issues
    content = re.sub(r'^(\d+)\.\s+\*\*([^*\n]+)\*\*(.+)$', r'\1. **\2**\3', content, flags=re.MULTILINE)
    
    # Fix lists with missing formatting
    content = re.sub(r'^(\*\*\d+)\.\s+\*\*([^*\n]+)$', r'\1. \2**', content, flags=re.MULTILINE)
    
    # Clean up extra whitespace and fix line spacing
    lines = content.split('\n')
    fixed_lines = []
    
    for i, line in enumerate(lines):
        # Skip empty lines at start
        if not fixed_lines and not line.strip():
            continue
            
        # Fix numbered lists that got broken
        if re.match(r'^\*\*(\d+)', line):
            # This is a broken numbered list
            match = re.match(r'^\*\*(\d+)\.\s+(.+)', line)
            if match:
                num, rest = match.groups()
                # Remove extra asterisks and format properly
                rest = re.sub(r'\*\*([^*]+)\*\*', r'**\1**', rest)
                fixed_lines.append(f'{num}. {rest}')
                continue
        
        # Fix lines with trailing asterisks
        line = re.sub(r'([^*])\*\*\s*$', r'\1', line)
        
        # Fix double asterisks at line start for numbered lists
        line = re.sub(r'^\*\*(\d+\.\s+.*)', r'\1', line)
        
        fixed_lines.append(line)
    
    return '\n'.join(fixed_lines)

def process_markdown_files():
    """Process all markdown files in the docs directory"""
    docs_dir = '/home/inocult/projects/studio3-docs/docs'
    
    # Find all markdown files
    markdown_files = []
    for root, dirs, files in os.walk(docs_dir):
        for file in files:
            if file.endswith('.md'):
                markdown_files.append(os.path.join(root, file))
    
    print(f"Found {len(markdown_files)} markdown files")
    
    total_fixes = 0
    files_fixed = 0
    
    for file_path in markdown_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                original_content = f.read()
            
            fixed_content = fix_markdown_issues(original_content)
            
            if fixed_content != original_content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(fixed_content)
                
                files_fixed += 1
                
                # Count differences
                orig_lines = original_content.split('\n')
                fixed_lines = fixed_content.split('\n')
                changes = sum(1 for a, b in zip(orig_lines, fixed_lines) if a != b)
                total_fixes += changes
                
                print(f"Fixed {changes} issues in {file_path}")
        
        except Exception as e:
            print(f"Error processing {file_path}: {e}")
    
    print(f"\nCompleted: {files_fixed} files fixed, {total_fixes} total issues resolved")

if __name__ == "__main__":
    process_markdown_files()