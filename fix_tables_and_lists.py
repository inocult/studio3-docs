#!/usr/bin/env python3
"""
Script to fix table formatting and list issues
"""

import os
import re
import glob
from pathlib import Path

def fix_table_formatting(content):
    """Fix table formatting issues"""
    
    lines = content.split('\n')
    result_lines = []
    
    for i, line in enumerate(lines):
        original_line = line
        
        # Fix table rows with unclosed bold markers like | **Text** | content |**
        if '|' in line and line.count('**') > 2:
            # Fix pattern: | **Text** | content |**
            line = re.sub(r'\|\s*\*\*([^*|]+)\*\*\s*\|\s*([^|]+)\s*\|\*\*', r'| **\1** | \2 |', line)
            
            # Fix pattern: |**Text** | -> | **Text** |
            line = re.sub(r'\|\*\*([^*|]+)\*\*\s*\|', r'| **\1** |', line)
            
            # Fix trailing ** at end of table rows
            line = re.sub(r'\|\*\*\s*$', r'|', line)
        
        # Fix numbered lists with unclosed bolds like "1. **Text** (40%)**"
        if re.match(r'^\d+\.\s+\*\*[^*]+\*\*.*\*\*.*$', line):
            # Remove trailing ** 
            line = re.sub(r'^(\d+\.\s+\*\*[^*]+\*\*[^*]*)\*\*(.*)$', r'\1\2', line)
        
        result_lines.append(line)
    
    return '\n'.join(result_lines)

def fix_list_spacing(content):
    """Fix list spacing and formatting issues"""
    
    lines = content.split('\n')
    result_lines = []
    prev_line = ""
    
    for i, line in enumerate(lines):
        stripped = line.strip()
        prev_stripped = prev_line.strip()
        
        # Add blank line before lists that start with bold markers
        if (re.match(r'^[-*]\s+\*\*[^*]+\*\*', stripped) and 
            prev_stripped and 
            not prev_stripped.startswith(('-', '*')) and
            not prev_stripped == '' and
            not prev_stripped.startswith('#')):
            result_lines.append('')
        
        # Fix double spaces after opening bold in lists
        line = re.sub(r'^(\s*[-*]\s+)\*\*\s{2,}([^*]+)\*\*', r'\1**\2**', line)
        
        result_lines.append(line)
        prev_line = line
    
    return '\n'.join(result_lines)

def fix_specific_patterns(content):
    """Fix specific problematic patterns found in the linting"""
    
    # Fix "**Daily Playbook:** Morning (2 hours)** Status update" pattern
    content = re.sub(r'(\*\*[^*]+:\*\*\s+[^*]+)\*\*\s+', r'\1\n\n', content)
    
    # Fix numbered sections like "2.**The Flood** (Hours 2" -> "2. **The Flood** (Hours 2"
    content = re.sub(r'^(\d+\.)\*\*([^*]+)\*\*', r'\1 **\2**', content, flags=re.MULTILINE)
    
    # Fix patterns like "1.**Transparency**: Document decisions**2. **Consistency""
    content = re.sub(r'(\d+\.)\*\*([^*]+):\*\*\s+([^*]+)\*\*(\d+\.)', r'\1 **\2:** \3\n\n\4', content)
    
    # Fix missing colons after bold headers
    content = re.sub(r'^\*\*([^*:]+)\*\*([A-Z][^*\n])', r'**\1:** \2', content, flags=re.MULTILINE)
    
    return content

def fix_code_blocks(content):
    """Fix code block formatting issues"""
    
    # Fix code blocks that got broken by bold fixing
    content = re.sub(r'```\*\*', r'```', content)
    content = re.sub(r'\*\*```', r'```', content)
    
    # Fix function definitions in code blocks
    content = re.sub(r'^\*\*def ([^*]+):\*\*\*\*$', r'def \1:', content, flags=re.MULTILINE)
    
    return content

def fix_file(filepath):
    """Fix tables and lists in a single file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            original_content = f.read()
        
        fixed_content = fix_table_formatting(original_content)
        fixed_content = fix_list_spacing(fixed_content)
        fixed_content = fix_specific_patterns(fixed_content)
        fixed_content = fix_code_blocks(fixed_content)
        
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
    """Fix tables and lists in all markdown files"""
    docs_dir = 'docs'
    md_files = glob.glob(os.path.join(docs_dir, '**/*.md'), recursive=True)
    
    print(f"Processing {len(md_files)} markdown files for table and list fixes...")
    
    fixed_count = 0
    for filepath in sorted(md_files):
        if fix_file(filepath):
            fixed_count += 1
    
    print(f"\nCompleted: {fixed_count} files modified")

if __name__ == "__main__":
    main()