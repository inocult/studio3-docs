#!/usr/bin/env python3
"""
Fix broken list formatting patterns in markdown files.
"""

import os
import re

def fix_broken_lists_in_file(filepath):
    """Fix broken list patterns in a file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    fixed_lines = []
    i = 0
    fixes = 0
    
    while i < len(lines):
        line = lines[i]
        
        # Skip if this is a table line
        if '|' in line and i > 0 and '|' in lines[i-1]:
            fixed_lines.append(line)
            i += 1
            continue
        
        # Pattern 1: Fix "* **Text" at start of line to "- **Text**"
        if re.match(r'^\*\s+\*\*([^*]+)$', line):
            match = re.match(r'^\*\s+\*\*([^*]+)$', line)
            fixed_line = f"- **{match.group(1).strip()}**\n"
            fixed_lines.append(fixed_line)
            fixes += 1
            i += 1
            continue
        
        # Pattern 2: Handle orphaned ** followed by list continuation
        if line.strip() == '**' and i + 1 < len(lines):
            next_line = lines[i + 1]
            if re.match(r'^\*\s+([^*].*)$', next_line):
                # Skip the orphaned ** and fix the next line
                match = re.match(r'^\*\s+([^*].*)$', next_line)
                content = match.group(1).strip()
                # Check if previous line has unfinished bold
                if i > 0 and re.search(r'\*\*[^*]+$', fixed_lines[-1]):
                    # Complete the bold on previous line
                    fixed_lines[-1] = fixed_lines[-1].rstrip() + '** ' + content + '\n'
                else:
                    fixed_lines.append(f"- {content}\n")
                fixes += 2
                i += 2
                continue
        
        # Pattern 3: Fix lines ending with incomplete bold "**text"
        if re.search(r'\*\*[^*]+$', line) and not line.strip().endswith('**'):
            fixed_line = re.sub(r'(\*\*[^*]+)$', r'\1**', line)
            fixed_lines.append(fixed_line)
            fixes += 1
            i += 1
            continue
        
        # Default: keep line as is
        fixed_lines.append(line)
        i += 1
    
    if fixes > 0:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.writelines(fixed_lines)
        print(f"Fixed {fixes} issues in {filepath}")
        return fixes
    
    return 0

def main():
    """Walk through docs directory and fix broken lists."""
    docs_dir = '/home/inocult/projects/studio3-docs/docs'
    total_fixes = 0
    files_fixed = 0
    
    for root, dirs, files in os.walk(docs_dir):
        for file in files:
            if file.endswith('.md'):
                filepath = os.path.join(root, file)
                fixes = fix_broken_lists_in_file(filepath)
                if fixes > 0:
                    total_fixes += fixes
                    files_fixed += 1
    
    print(f"\nSummary: Fixed {total_fixes} issues across {files_fixed} files")

if __name__ == "__main__":
    main()