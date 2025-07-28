#!/usr/bin/env python3
"""
Fix trailing double asterisks and other malformed patterns
"""

import os
import re
import glob
from pathlib import Path

def fix_trailing_patterns(content):
    """Fix all trailing asterisk patterns and other malformed markdown"""
    fixes_count = 0
    
    # Pattern 1: **text** some text** → **text** some text
    # Match proper bold followed by text and exactly 2 trailing asterisks at line end
    pattern1 = re.compile(r'(\*\*[^*]+\*\*)([^*]+)\*{2}\s*$', re.MULTILINE)
    matches = pattern1.findall(content)
    if matches:
        content = pattern1.sub(r'\1 \2', content)
        fixes_count += len(matches)
    
    # Pattern 2: -****text** → - **text**
    # Match dash followed by 4 asterisks
    pattern2 = re.compile(r'^(\s*)-\*{4}([^*]+)\*{2}', re.MULTILINE)
    matches = pattern2.findall(content)
    if matches:
        content = pattern2.sub(r'\1- **\2**', content)
        fixes_count += len(matches)
    
    # Pattern 3: text****text** → text **text**
    # Match text followed by 4 asterisks in middle of line
    pattern3 = re.compile(r'([^*\s])\*{4}([^*]+)\*{2}')
    matches = pattern3.findall(content)
    if matches:
        content = pattern3.sub(r'\1 **\2**', content)
        fixes_count += len(matches)
    
    # Pattern 4: **text:****text** → **text:** **text**
    # Special case for colons
    pattern4 = re.compile(r'(\*\*[^*]+:\*\*)\*{2}([^*]+)\*{2}')
    matches = pattern4.findall(content)
    if matches:
        content = pattern4.sub(r'\1 **\2**', content)
        fixes_count += len(matches)
    
    # Pattern 5: - **text** → (ensure space after dash)
    # Already handled in previous script but double-check
    pattern5 = re.compile(r'^(\s*)(-+)\*\*', re.MULTILINE)
    matches = pattern5.findall(content)
    if matches:
        content = pattern5.sub(r'\1\2 **', content)
        fixes_count += len(matches)
    
    # Pattern 6: **text* → **text**
    # Fix incomplete bold (single asterisk at end)
    pattern6 = re.compile(r'\*\*([^*\n]+)\*(?!\*)')
    matches = pattern6.findall(content)
    if matches:
        content = pattern6.sub(r'**\1**', content)
        fixes_count += len(matches)
    
    # Pattern 7: Fix lines that have alternating bold/normal/bold pattern with trailing **
    # Like: - **text** normal text**
    pattern7 = re.compile(r'^(\s*-\s*\*\*[^*]+\*\*)\s+([^*]+)\*\*\s*$', re.MULTILINE)
    matches = pattern7.findall(content)
    if matches:
        content = pattern7.sub(r'\1 \2', content)
        fixes_count += len(matches)
    
    return content, fixes_count

def process_file(file_path):
    """Process a single markdown file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Apply fixes
        fixed_content, fixes = fix_trailing_patterns(content)
        
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
    
    print("🔧 Fixing trailing asterisks and malformed patterns...")
    print("Patterns being fixed:")
    print("  - **text** extra text** → **text** extra text")
    print("  - -****text** → - **text**")
    print("  - text****text** → text **text**")
    print("  - **text:****text** → **text:** **text**")
    print()
    
    # Process all markdown files
    for md_file in sorted(docs_dir.rglob("*.md")):
        fixes = process_file(md_file)
        if fixes > 0:
            total_fixes += fixes
            files_processed += 1
    
    print(f"\n🎉 Trailing asterisk fix complete!")
    print(f"   📁 Files updated: {files_processed}")
    print(f"   🔧 Total fixes: {total_fixes}")

if __name__ == "__main__":
    main()