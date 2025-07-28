#!/usr/bin/env python3
"""
Script to fix common markdown formatting patterns across all files
"""

import os
import re
import glob
from pathlib import Path

def fix_common_patterns(content):
    """Fix the most common markdown formatting issues"""
    
    # Fix broken bold markers like "- ** text" -> "- **text**"
    content = re.sub(r'^(\s*[-*]\s+)\*\*\s+([^*\n]+)$', r'\1**\2**', content, flags=re.MULTILINE)
    
    # Fix unclosed bold at start of lists like "- ** text" where text continues on next line
    content = re.sub(r'^(\s*[-*]\s+)\*\*\s+', r'\1**', content, flags=re.MULTILINE)
    
    # Fix patterns like "**Section:** Content" -> "**Section:**\n\n**Content**"
    content = re.sub(r'\*\*([^*]+):\*\*\s+([A-Z][^*\n]+)$', r'**\1:**\n\n**\2**', content, flags=re.MULTILINE)
    
    # Fix unclosed section headers like "**Section" -> "**Section**"
    content = re.sub(r'^\*\*([^*\n]+)$', r'**\1**', content, flags=re.MULTILINE)
    
    # Fix code blocks with unclosed bold like "** def" -> "**def"
    content = re.sub(r'^\*\*\s+def ', r'**def ', content, flags=re.MULTILINE)
    
    # Fix missing spaces after colons in examples (but not in URLs)
    content = re.sub(r'\*\*Example:"', r'**Example:** "', content)
    
    # Add blank lines before sections that start with **
    lines = content.split('\n')
    result_lines = []
    prev_line = ""
    
    for i, line in enumerate(lines):
        stripped = line.strip()
        
        # Add blank line before bold headers if previous line isn't blank
        if (stripped.startswith('**') and stripped.endswith('**') and 
            prev_line.strip() and not prev_line.strip().startswith('**') and
            not prev_line.strip().startswith('#')):
            result_lines.append('')
        
        result_lines.append(line)
        prev_line = line
    
    return '\n'.join(result_lines)

def fix_file(filepath):
    """Fix common patterns in a single file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            original_content = f.read()
        
        fixed_content = fix_common_patterns(original_content)
        
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
    """Fix common patterns in all markdown files"""
    docs_dir = 'docs'
    md_files = glob.glob(os.path.join(docs_dir, '**/*.md'), recursive=True)
    
    print(f"Processing {len(md_files)} markdown files...")
    
    fixed_count = 0
    for filepath in sorted(md_files):
        if fix_file(filepath):
            fixed_count += 1
    
    print(f"\nCompleted: {fixed_count} files modified")

if __name__ == "__main__":
    main()