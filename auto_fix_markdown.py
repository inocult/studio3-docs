#!/usr/bin/env python3
"""
Auto-fix common markdown formatting issues.
Can be run on individual files or entire directories.
"""

import os
import sys
import re
import glob

def fix_markdown_file(file_path):
    """Fix common formatting issues in a markdown file."""
    print(f"Fixing {file_path}...")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        lines = content.split('\n')
    
    fixed_lines = []
    in_code_block = False
    in_arena_card = False
    modified = False
    i = 0
    
    while i < len(lines):
        line = lines[i]
        
        # Track code blocks - don't modify content inside them
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
        
        # Don't modify lines inside code blocks
        if in_code_block:
            fixed_lines.append(line)
            i += 1
            continue
        
        original_line = line
        
        # Fix space after opening bold marker: ** text -> **text
        line = re.sub(r'\*\*\s+([^*])', r'**\1', line)
        
        # Fix space before closing bold marker: text ** -> text**
        line = re.sub(r'([^*])\s+\*\*', r'\1**', line)
        
        # Fix missing space after colon (but not in URLs or time formats)
        line = re.sub(r'(?<!http)(?<!https)(?<!\d):(?![/\d])(?!\s)', ': ', line)
        
        # Fix unclosed bold markers - add ** at end if odd count
        star_count = line.count('**')
        if star_count % 2 == 1 and line.strip() and not line.strip().endswith('**'):
            line = line.rstrip() + '**'
        
        # Fix bold header with colon needing blank line before list
        if re.match(r'^\s*\*\*[^*]+\*\*:\s*$', line.strip()):
            # Check if next line is a list
            next_idx = i + 1
            while next_idx < len(lines) and not lines[next_idx].strip():
                next_idx += 1
            
            if next_idx < len(lines):
                next_line = lines[next_idx].strip()
                if re.match(r'^[-*\d]', next_line) or re.match(r'^\d+\.', next_line):
                    # Check if there's already a blank line
                    if i + 1 < len(lines) and not lines[i + 1].strip():
                        # Already has blank line
                        pass
                    else:
                        # Add blank line
                        fixed_lines.append(line)
                        fixed_lines.append('')
                        modified = True
                        i += 1
                        continue
        
        # Check if we modified the line
        if line != original_line:
            modified = True
        
        fixed_lines.append(line)
        i += 1
    
    if modified:
        # Write back the fixed content
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(fixed_lines))
        print(f"  ✅ Fixed formatting issues")
        return True
    else:
        print(f"  ✓ No issues found")
        return False

def main():
    """Main function."""
    if len(sys.argv) < 2:
        print("Usage: python3 auto_fix_markdown.py <file_or_directory>")
        print("Examples:")
        print("  python3 auto_fix_markdown.py docs/anchors-guide/anchor-council.md")
        print("  python3 auto_fix_markdown.py docs/")
        return 1
    
    target = sys.argv[1]
    
    if os.path.isfile(target) and target.endswith('.md'):
        # Single file
        fix_markdown_file(target)
    elif os.path.isdir(target):
        # Directory - find all .md files
        md_files = glob.glob(os.path.join(target, '**/*.md'), recursive=True)
        fixed_count = 0
        for file_path in sorted(md_files):
            if fix_markdown_file(file_path):
                fixed_count += 1
        print(f"\nFixed {fixed_count} files out of {len(md_files)} total")
    else:
        print(f"Error: {target} is not a valid markdown file or directory")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())