#!/usr/bin/env python3
"""
Fix malformed markdown patterns like ****text**, -**text**, and similar issues
"""

import os
import re
import glob
from pathlib import Path

def fix_malformed_patterns(content):
    """Fix all malformed markdown patterns"""
    fixes_count = 0
    
    # Pattern 1: -**text** → - **text**
    # Match dash directly followed by asterisks
    pattern1 = re.compile(r'^(\s*)-\*\*', re.MULTILINE)
    if pattern1.search(content):
        content = pattern1.sub(r'\1- **', content)
        fixes_count += len(pattern1.findall(content))
    
    # Pattern 2: ****text** → **text**
    # Match 4 asterisks followed by text and 2 asterisks
    pattern2 = re.compile(r'\*{4}([^*]+)\*{2}')
    if pattern2.search(content):
        content = pattern2.sub(r'**\1**', content)
        fixes_count += len(pattern2.findall(content))
    
    # Pattern 3: **text**** → **text**
    # Match 2 asterisks, text, then 4 asterisks
    pattern3 = re.compile(r'\*{2}([^*]+)\*{4}')
    if pattern3.search(content):
        content = pattern3.sub(r'**\1**', content)
        fixes_count += len(pattern3.findall(content))
    
    # Pattern 4: -****text** → - **text**
    # Match dash followed by 4 asterisks
    pattern4 = re.compile(r'^(\s*)-\*{4}([^*]+)\*{2}', re.MULTILINE)
    if pattern4.search(content):
        content = pattern4.sub(r'\1- **\2**', content)
        fixes_count += len(pattern4.findall(content))
    
    # Pattern 5: **text** extra text** → **text** extra text
    # Match proper bold followed by text and trailing asterisks
    pattern5 = re.compile(r'(\*\*[^*]+\*\*)([^*\n]+)\*\*\s*$', re.MULTILINE)
    if pattern5.search(content):
        content = pattern5.sub(r'\1 \2', content)
        fixes_count += len(pattern5.findall(content))
    
    # Pattern 6: Multiple consecutive asterisks (6 or more)
    pattern6 = re.compile(r'\*{6,}')
    if pattern6.search(content):
        content = pattern6.sub('**', content)
        fixes_count += len(pattern6.findall(content))
    
    # Pattern 7: **text* → **text**
    # Incomplete bold patterns
    pattern7 = re.compile(r'\*\*([^*\n]+)\*(?!\*)')
    if pattern7.search(content):
        content = pattern7.sub(r'**\1**', content)
        fixes_count += len(pattern7.findall(content))
    
    # Pattern 8: Numbered list without space after period
    pattern8 = re.compile(r'^(\s*\d+\.)([^\s])', re.MULTILINE)
    if pattern8.search(content):
        content = pattern8.sub(r'\1 \2', content)
        fixes_count += len(pattern8.findall(content))
    
    # Pattern 9: Empty bold markers ** **
    pattern9 = re.compile(r'\*\*\s+\*\*')
    if pattern9.search(content):
        content = pattern9.sub('', content)
        fixes_count += len(pattern9.findall(content))
    
    return content, fixes_count

def process_file(file_path):
    """Process a single markdown file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Apply fixes
        fixed_content, fixes = fix_malformed_patterns(content)
        
        if fixes > 0:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(fixed_content)
            print(f"✅ {file_path}: {fixes} fixes applied")
            return fixes
        
        return 0
        
    except Exception as e:
        print(f"❌ Error processing {file_path}: {e}")
        return 0

def main():
    """Process all markdown files"""
    docs_dir = Path("docs")
    total_fixes = 0
    files_processed = 0
    
    print("🔧 Fixing malformed markdown patterns...")
    print("Patterns being fixed:")
    print("  - -**text** → - **text**")
    print("  - ****text** → **text**")
    print("  - **text**** → **text**")
    print("  - **text** extra** → **text** extra")
    print("  - **text* → **text**")
    print()
    
    # Process all markdown files
    for md_file in sorted(docs_dir.rglob("*.md")):
        fixes = process_file(md_file)
        if fixes > 0:
            total_fixes += fixes
            files_processed += 1
    
    print(f"\n🎉 Malformed markdown fix complete!")
    print(f"   📁 Files updated: {files_processed}")
    print(f"   🔧 Total fixes: {total_fixes}")

if __name__ == "__main__":
    main()