#!/usr/bin/env python3
"""
Script to fix unclosed bold markers across all files
"""

import os
import re
import glob
from pathlib import Path

def fix_unclosed_bolds(content):
    """Fix unclosed bold markers in markdown content"""
    
    lines = content.split('\n')
    result_lines = []
    
    for i, line in enumerate(lines):
        # Fix pattern: "- **text" at end of line (unclosed bold in list)
        if re.match(r'^(\s*[-*]\s+)\*\*([^*\n]+)$', line):
            # Check if this is the last item in a series or standalone
            line = re.sub(r'^(\s*[-*]\s+)\*\*([^*\n]+)$', r'\1**\2**', line)
        
        # Fix pattern: "**Text" at start of line (section header)
        elif re.match(r'^\*\*([^*\n]+)$', line):
            # Only close if it's not followed by more content
            if i + 1 < len(lines) and not lines[i + 1].strip().startswith('-'):
                line = f"**{line[2:]}**"
        
        # Fix pattern: "** Text:" at start (bold header with colon)
        elif re.match(r'^\*\*\s*([^*\n]+):$', line):
            line = re.sub(r'^\*\*\s*([^*\n]+):$', r'**\1:**', line)
        
        # Fix broken patterns in specific contexts
        elif '**def guide_technical_decisions():' in line:
            line = line.replace('**def guide_technical_decisions():', '**def guide_technical_decisions():**')
        
        result_lines.append(line)
    
    return '\n'.join(result_lines)

def fix_specific_patterns(content):
    """Fix specific problematic patterns"""
    
    # Fix the specific example issue
    content = re.sub(r'\*\*Example:\s*"([^"]+)"\*\*', r'**Example:** "\1"', content)
    
    # Fix pattern where bold continues across lines incorrectly
    content = re.sub(r'(\*\*[^*\n]+)\n([^-*\n][^*]*\*\*)', r'\1**\n\2', content)
    
    # Fix common section headers that should be closed
    patterns = [
        (r'^\*\* ([^:*\n]+):$', r'**\1:**'),
        (r'^(\*\*[^*\n]+)(?!\*\*)$', r'\1**'),
    ]
    
    for pattern, replacement in patterns:
        content = re.sub(pattern, replacement, content, flags=re.MULTILINE)
    
    return content

def fix_file(filepath):
    """Fix unclosed bolds in a single file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            original_content = f.read()
        
        fixed_content = fix_unclosed_bolds(original_content)
        fixed_content = fix_specific_patterns(fixed_content)
        
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
    """Fix unclosed bolds in all markdown files"""
    docs_dir = 'docs'
    md_files = glob.glob(os.path.join(docs_dir, '**/*.md'), recursive=True)
    
    print(f"Processing {len(md_files)} markdown files for unclosed bolds...")
    
    fixed_count = 0
    for filepath in sorted(md_files):
        if fix_file(filepath):
            fixed_count += 1
    
    print(f"\nCompleted: {fixed_count} files modified")

if __name__ == "__main__":
    main()