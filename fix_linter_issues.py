#!/usr/bin/env python3
"""
Fix specific linter-identified markdown issues.
"""

import os
import re
from pathlib import Path

def fix_linter_issues(content, file_path):
    """Fix specific linter-identified markdown patterns."""
    lines = content.split('\n')
    fixed_lines = []
    changes_made = 0
    
    for i, line in enumerate(lines):
        original_line = line
        
        # Fix double bold patterns like: ****text** content****
        line = re.sub(r'\*\*\*\*([^*]+)\*\*([^*]*)\*\*\*\*', r'**\1:** \2', line)
        if line != original_line:
            changes_made += 1
            original_line = line
        
        # Fix patterns like: -****text** content****
        line = re.sub(r'-\s*\*\*\*\*([^*]+)\*\*([^*]*)\*\*\*\*', r'- **\1:** \2', line)
        if line != original_line:
            changes_made += 1
            original_line = line
        
        # Fix broken numbered lists: **1.**text:**
        line = re.sub(r'^\*\*(\d+)\.\*\*([^:]*):?\*\*', r'\1. **\2:**', line)
        if line != original_line:
            changes_made += 1
            original_line = line
        
        # Fix broken numbered lists: **1. text
        line = re.sub(r'^\*\*(\d+)\.\s*([^*]+)$', r'\1. \2', line)
        if line != original_line:
            changes_made += 1
            original_line = line
        
        # Fix double asterisks in arena cards and divs that break formatting
        if any(marker in line for marker in ['<div class="arena-card"', '</div>', '```']):
            # Clean multiple asterisks that break formatting
            line = re.sub(r'\*{5,}', '**', line)
            if line != original_line:
                changes_made += 1
                original_line = line
        
        # Fix patterns like: text****</div>**## Header
        line = re.sub(r'([a-zA-Z])\*\*\*\*</div>\*\*##\s*([A-Z])', r'\1</div>\n\n## \2', line)
        if line != original_line:
            changes_made += 1
            original_line = line
        
        # Fix mixed bold/numbered patterns: 5.**text** → content****
        line = re.sub(r'(\d+)\.\*\*([^*]+)\*\*\s*→\s*([^*]*)\*\*\*\*', r'\1. **\2** → \3', line)
        if line != original_line:
            changes_made += 1
            original_line = line
        
        # Fix standalone numbered patterns: **1.**
        line = re.sub(r'^\*\*(\d+)\.\*\*\s*$', r'\1.', line)
        if line != original_line:
            changes_made += 1
            original_line = line
        
        # Fix patterns where bold markers are broken across elements
        # Pattern: text****other text**
        line = re.sub(r'([a-zA-Z])\*\*\*\*([^*]+)\*\*', r'\1**\n- **\2**', line)
        if line != original_line:
            changes_made += 1
        
        fixed_lines.append(line)
    
    return '\n'.join(fixed_lines), changes_made

def main():
    """Process all markdown files to fix linter issues."""
    docs_dir = Path("docs")
    total_changes = 0
    files_processed = 0
    
    print("🔧 Fixing linter-identified issues...")
    
    for md_file in docs_dir.rglob("*.md"):
        try:
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            fixed_content, changes = fix_linter_issues(content, str(md_file))
            
            if changes > 0:
                with open(md_file, 'w', encoding='utf-8') as f:
                    f.write(fixed_content)
                
                print(f"  ✅ {md_file}: {changes} fixes")
                total_changes += changes
                files_processed += 1
            
        except Exception as e:
            print(f"  ❌ Error processing {md_file}: {e}")
    
    print(f"\n🎉 Linter fix complete!")
    print(f"   📁 Files processed: {files_processed}")
    print(f"   🔧 Total fixes: {total_changes}")

if __name__ == "__main__":
    main()