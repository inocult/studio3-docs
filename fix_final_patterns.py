#!/usr/bin/env python3
"""
Fix the final broken numbered list patterns created by the previous script.
Specifically targets patterns like **1. **Text** format.
"""

import os
import re
import glob

def fix_file_content(content, file_path):
    """Fix the specific numbered list patterns that are broken"""
    original_content = content
    fixes_count = 0
    
    # Fix patterns like "**1. **Text** → Something"
    # This should become "1. **Text** → Something"
    pattern1 = r'\*\*(\d+)\.\s+\*\*([^*]+)\*\*\s*→\s*([^\n]+)'
    matches = re.findall(pattern1, content)
    if matches:
        print(f"  Found {len(matches)} numbered arrow patterns")
        content = re.sub(pattern1, r'\1. **\2** → \3', content)
        fixes_count += len(matches)
    
    # Fix patterns like "**1. **Text"
    # This should become "1. **Text**"
    pattern2 = r'\*\*(\d+)\.\s+\*\*([^*\n]+)$'
    matches = re.findall(pattern2, content, re.MULTILINE)
    if matches:
        print(f"  Found {len(matches)} numbered list start patterns")
        content = re.sub(pattern2, r'\1. **\2**', content, flags=re.MULTILINE)
        fixes_count += len(matches)
    
    # Fix patterns where we have "**   " at the start of lines (broken bullet lists)
    pattern3 = r'^\*\*(\s+)'
    matches = re.findall(pattern3, content, re.MULTILINE)
    if matches:
        print(f"  Found {len(matches)} broken bullet patterns")
        content = re.sub(pattern3, r'\1', content, flags=re.MULTILINE)
        fixes_count += len(matches)
    
    # Fix the specific pattern: "**Technical Specifications:** Minimum Stake:**" 
    pattern4 = r'\*\*([^*:]+):\*\*\s*([^*\n]+):\*\*'
    matches = re.findall(pattern4, content)
    if matches:
        print(f"  Found {len(matches)} double colon specification patterns")
        content = re.sub(pattern4, r'**\1:**\n- **\2:**', content)
        fixes_count += len(matches)
    
    # Fix patterns like "**Time Bonus (Early Signals):" without closing **
    pattern5 = r'\*\*([^*\n]+):\n'
    lines = content.split('\n')
    for i, line in enumerate(lines):
        if re.match(r'\*\*([^*\n]+):$', line):
            lines[i] = f"**{re.match(r'\*\*([^*\n]+):$', line).group(1)}:**"
            fixes_count += 1
            print(f"  Fixed missing closing ** in line: {line[:50]}...")
    content = '\n'.join(lines)
    
    return content, fixes_count

def main():
    """Process all markdown files and fix formatting issues"""
    docs_dir = 'docs'
    total_fixes = 0
    files_processed = 0
    
    print("🔧 Fixing final markdown patterns...")
    
    # Get all markdown files
    md_files = []
    for root, dirs, files in os.walk(docs_dir):
        for file in files:
            if file.endswith('.md'):
                md_files.append(os.path.join(root, file))
    
    for file_path in sorted(md_files):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            fixed_content, fixes_count = fix_file_content(content, file_path)
            
            if fixes_count > 0:
                print(f"📝 {file_path}: {fixes_count} fixes")
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(fixed_content)
                total_fixes += fixes_count
                files_processed += 1
            
        except Exception as e:
            print(f"❌ Error processing {file_path}: {e}")
    
    print(f"\n✅ Complete! Fixed {total_fixes} issues across {files_processed} files")

if __name__ == "__main__":
    main()