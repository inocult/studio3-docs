#!/usr/bin/env python3
"""
Comprehensive fix for all remaining markdown formatting issues.
Targets the specific patterns seen in get-started.md and similar pages.
"""

import os
import re

def fix_file_content(content, file_path):
    """Fix all remaining broken patterns comprehensively"""
    original_content = content
    fixes_count = 0
    
    # Fix broken numbered lists that start without "1."
    # Pattern: "Some text 2. **Next item" should be "1. Some text\n2. **Next item"
    lines = content.split('\n')
    for i, line in enumerate(lines):
        # Look for lines that start with "2." without a proper "1." before
        if re.match(r'^.+\s+2\.\s+\*\*', line):
            # Split the line at "2." 
            parts = line.split(' 2. ', 1)
            if len(parts) == 2:
                lines[i] = f"1. {parts[0].strip()}\n2. {parts[1]}"
                fixes_count += 1
                print(f"  Fixed missing 1. in line: {line[:50]}...")
        
        # Fix lines that start with "3." without proper numbering
        elif re.match(r'^.+\s+3\.\s+\*\*', line):
            parts = line.split(' 3. ', 1)
            if len(parts) == 2:
                lines[i] = f"2. {parts[0].strip()}\n3. {parts[1]}"
                fixes_count += 1
                print(f"  Fixed missing 2. in line: {line[:50]}...")
    
    content = '\n'.join(lines)
    
    # Fix missing closing ** in "**Text:" patterns
    content = re.sub(r'\*\*([^*\n]+):\s*$', r'**\1:**', content, flags=re.MULTILINE)
    if re.search(r'\*\*([^*\n]+):\s*$', original_content, flags=re.MULTILINE):
        fixes_count += content.count(':**') - original_content.count(':**')
        print(f"  Fixed missing closing ** in headers")
    
    # Fix broken bullet lists like "**- item"
    pattern = r'^\*\*-\s+([^\n]+)'
    matches = re.findall(pattern, content, re.MULTILINE)
    if matches:
        content = re.sub(pattern, r'- **\1**', content, flags=re.MULTILINE)
        fixes_count += len(matches)
        print(f"  Fixed {len(matches)} broken bullet patterns (**-)")
    
    # Fix numbered lists that are broken like "**1. **Text" to "1. **Text**"
    pattern = r'^\*\*(\d+)\.\s+\*\*([^*\n]+)$'
    matches = re.findall(pattern, content, re.MULTILINE)
    if matches:
        content = re.sub(pattern, r'\1. **\2**', content, flags=re.MULTILINE)
        fixes_count += len(matches)
        print(f"  Fixed {len(matches)} broken numbered list patterns")
    
    # Fix patterns like "**Text **" (extra space before closing)
    pattern = r'\*\*([^*]+)\s+\*\*'
    matches = re.findall(pattern, content)
    if matches:
        content = re.sub(pattern, r'**\1**', content)
        fixes_count += len(matches)
        print(f"  Fixed {len(matches)} patterns with extra spaces")
    
    # Fix missing closing ** in sections like "**If you have:** **- item"
    lines = content.split('\n')
    for i, line in enumerate(lines):
        # Look for lines ending with ":** **-"
        if re.search(r'\*\*([^*:]+):\*\*\s+\*\*-', line):
            # Fix to proper format
            fixed_line = re.sub(r'\*\*([^*:]+):\*\*\s+\*\*-\s*([^\n]+)', r'**\1:**\n- **\2**', line)
            if fixed_line != line:
                lines[i] = fixed_line
                fixes_count += 1
                print(f"  Fixed broken list after header: {line[:50]}...")
    
    content = '\n'.join(lines)
    
    # Fix running text that should be separate numbered items
    # Pattern: "item 2. **next item 3. **third item"
    pattern = r'([^.\n]+)\s+(\d+)\.\s+\*\*([^*\n]+)\*\*\s+(\d+)\.\s+\*\*([^*\n]+)'
    matches = re.findall(pattern, content)
    if matches:
        for match in matches:
            old_text = f"{match[0]} {match[1]}. **{match[2]}** {match[3]}. **{match[4]}"
            new_text = f"1. {match[0].strip()}\n{match[1]}. **{match[2]}**\n{match[3]}. **{match[4]}**"
            content = content.replace(old_text, new_text)
            fixes_count += 1
            print(f"  Fixed running numbered items")
    
    # Fix incomplete bullet lists that end with "**"
    pattern = r'^-\s+([^*\n]+)\s+\*\*\s*$'
    matches = re.findall(pattern, content, re.MULTILINE)
    if matches:
        content = re.sub(pattern, r'- **\1**', content, flags=re.MULTILINE)
        fixes_count += len(matches)
        print(f"  Fixed {len(matches)} incomplete bullet lists")
    
    # Fix long running lists that should be properly formatted
    # Look for patterns like "item1 - item2 - item3" and make them proper lists
    lines = content.split('\n')
    for i, line in enumerate(lines):
        if ' - ' in line and not line.strip().startswith('-'):
            # Check if it's a long line with multiple " - " separators
            parts = line.split(' - ')
            if len(parts) >= 3:  # At least 3 items
                # Convert to proper bullet list
                new_lines = []
                for j, part in enumerate(parts):
                    if j == 0:
                        new_lines.append(f"- {part.strip()}")
                    else:
                        new_lines.append(f"- {part.strip()}")
                lines[i] = '\n'.join(new_lines)
                fixes_count += 1
                print(f"  Fixed long running list into proper bullets")
    
    content = '\n'.join(lines)
    
    return content, fixes_count

def main():
    """Process all markdown files and fix comprehensive patterns"""
    docs_dir = 'docs'
    total_fixes = 0
    files_processed = 0
    
    print("🔧 Running comprehensive markdown pattern fixes...")
    
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