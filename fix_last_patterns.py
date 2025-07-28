#!/usr/bin/env python3
"""
Fix the remaining specific broken patterns in the markdown files.
"""

import os
import re

def fix_file_content(content, file_path):
    """Fix the remaining broken patterns"""
    original_content = content
    fixes_count = 0
    
    # Fix incomplete numbered lists and headings that are cut off
    lines = content.split('\n')
    for i, line in enumerate(lines):
        fixed_line = line
        
        # Fix patterns like "2. **Market Signals"  (missing closing **)
        if re.match(r'^\d+\.\s+\*\*([^*]+)$', line):
            match = re.match(r'^\d+\.\s+\*\*([^*]+)$', line)
            fixed_line = f"{line}**"
            fixes_count += 1
            print(f"  Fixed missing ** in: {line}")
        
        # Fix patterns like "3. **Milestone Factors" (missing closing **)
        elif re.match(r'^\s*\d+\.\s+\*\*([^*]+)$', line):
            match = re.match(r'^\s*\d+\.\s+\*\*([^*]+)$', line)
            fixed_line = f"{line}**"
            fixes_count += 1
            print(f"  Fixed missing ** in: {line}")
        
        # Fix patterns like "**2. **Technical Issues" (remove first **)
        elif re.match(r'^\*\*(\d+)\.\s+\*\*([^*\n]+)$', line):
            match = re.match(r'^\*\*(\d+)\.\s+\*\*([^*\n]+)$', line)
            fixed_line = f"{match.group(1)}. **{match.group(2)}**"
            fixes_count += 1
            print(f"  Fixed double ** pattern: {line}")
        
        # Fix patterns like "**2. **Team Problems" (remove first **)
        elif re.match(r'^\*\*(\d+)\.\s+\*\*([^*]+)$', line):
            match = re.match(r'^\*\*(\d+)\.\s+\*\*([^*]+)$', line)
            fixed_line = f"{match.group(1)}. **{match.group(2)}**"
            fixes_count += 1
            print(f"  Fixed incomplete ** pattern: {line}")
            
        lines[i] = fixed_line
    
    content = '\n'.join(lines)
    
    # Fix patterns where numbered lists run together
    content = re.sub(r'(\d+)\.\s+\*\*([^*]+)\*\*\s*(\d+)\.\s+\*\*([^*]+)', 
                     r'\1. **\2**\n\3. **\4**', content)
    
    # Fix patterns where numbered lists have missing **
    content = re.sub(r'(\d+)\.\s+\*\*([^*\n]+)$', r'\1. **\2**', content, flags=re.MULTILINE)
    
    return content, fixes_count

def main():
    """Process all markdown files and fix remaining patterns"""
    docs_dir = 'docs'
    total_fixes = 0
    files_processed = 0
    
    print("🔧 Fixing last remaining markdown patterns...")
    
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