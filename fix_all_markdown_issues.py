#!/usr/bin/env python3
"""
Comprehensive fix for all markdown formatting issues.
"""

import os
import re

def fix_markdown_comprehensive(filepath):
    """Fix all types of markdown formatting issues."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    
    # Fix pattern: **text\n** on separate line followed by list continuation
    content = re.sub(r'\*\*([^*\n]+)\n\*\*\n+\*\s+', r'**\1** ', content, flags=re.MULTILINE)
    
    # Fix pattern: **text without closing **
    content = re.sub(r'\*\*([^*\n]+)$', r'**\1**', content, flags=re.MULTILINE)
    
    # Fix pattern: broken list with orphaned ** and * on next line
    content = re.sub(r'\n\*\*\n+\*\s+', r'** ', content)
    
    # Fix pattern: - **text\n**\n- * continuation
    content = re.sub(r'- \*\*([^*\n]+)\n\*\*\n- \*\s+', r'- **\1** ', content)
    
    # Fix pattern: - **text\n**\n* * continuation
    content = re.sub(r'- \*\*([^*\n]+)\n\*\*\n\*\s+\*\s+', r'- **\1** ', content)
    
    # Fix pattern: numbered lists with broken bold
    content = re.sub(r'(\d+\.) \*\*([^*\n]+)\n\*\*\*\s+\*\s+', r'\1 **\2** ', content)
    
    # Fix multiple line breaks between list items
    content = re.sub(r'\n{3,}', r'\n\n', content)
    
    # Fix table cells with orphaned **
    lines = content.split('\n')
    fixed_lines = []
    in_table = False
    
    for i, line in enumerate(lines):
        if '|' in line and i > 0 and '|' in lines[i-1]:
            in_table = True
        elif line.strip() == '' and in_table:
            in_table = False
            
        if line.strip() == '**' and not in_table:
            # Skip orphaned ** outside tables
            continue
        else:
            fixed_lines.append(line)
    
    content = '\n'.join(fixed_lines)
    
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def main():
    """Process all markdown files."""
    docs_dir = '/home/inocult/projects/studio3-docs/docs'
    fixed_count = 0
    
    for root, dirs, files in os.walk(docs_dir):
        for file in files:
            if file.endswith('.md'):
                filepath = os.path.join(root, file)
                if fix_markdown_comprehensive(filepath):
                    print(f"Fixed: {filepath}")
                    fixed_count += 1
    
    print(f"\nTotal files fixed: {fixed_count}")

if __name__ == "__main__":
    main()