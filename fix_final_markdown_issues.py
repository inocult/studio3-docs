#!/usr/bin/env python3
"""
Final comprehensive markdown fix for Studio3 documentation.
Addresses remaining formatting issues found in manual review.
"""

import os
import re
from pathlib import Path

def fix_markdown_issues(content, file_path):
    """Fix markdown formatting issues in content."""
    lines = content.split('\n')
    fixed_lines = []
    changes_made = 0
    
    for i, line in enumerate(lines):
        original_line = line
        
        # Fix headers that are missing space or have extra asterisks
        if re.match(r'^\*\*#+\s', line):
            line = re.sub(r'^\*\*#+\s', lambda m: m.group(0)[2:], line)
            changes_made += 1
        
        # Fix broken bold patterns with multiple asterisks
        # Pattern: ****text**: content****
        line = re.sub(r'\*\*\*\*([^*:]+):\*\*([^*]+)\*\*\*\*', r'- **\1:** \2', line)
        if line != original_line:
            changes_made += 1
            original_line = line
        
        # Fix patterns like: -****text**: content**
        line = re.sub(r'-\s*\*\*\*\*([^*:]+):\*\*([^*]*)\*\*', r'- **\1:** \2', line)
        if line != original_line:
            changes_made += 1
            original_line = line
        
        # Fix patterns like: - **text**: content****
        line = re.sub(r'-\s*\*\*([^*:]+):\*\*([^*]*)\*\*\*\*', r'- **\1:** \2', line)
        if line != original_line:
            changes_made += 1
            original_line = line
        
        # Fix running numbered lists without proper line breaks
        # Pattern: something**2. **text**
        if re.search(r'\*\*\d+\.\s*\*\*', line) and not line.strip().startswith(('1.', '2.', '3.', '4.', '5.')):
            # Split on numbered items
            parts = re.split(r'(\*\*\d+\.\s*\*\*[^*]+\*\*)', line)
            if len(parts) > 1:
                new_lines = []
                for j, part in enumerate(parts):
                    if re.match(r'\*\*\d+\.\s*\*\*', part):
                        # Convert **2. **text** to 2. **text**
                        clean_part = re.sub(r'\*\*(\d+)\.\s*\*\*([^*]+)\*\*', r'\1. **\2**', part)
                        new_lines.append(clean_part)
                    elif part.strip():
                        new_lines.append(part)
                
                if len(new_lines) > 1:
                    # Add the first part to current line, rest as new lines
                    line = new_lines[0]
                    for new_line in new_lines[1:]:
                        fixed_lines.append(line)
                        line = new_line
                    changes_made += 1
        
        # Fix patterns where content runs together: content**something
        line = re.sub(r'([a-zA-Z])\*\*([A-Z][^*:]+:)', r'\1\n\n**\2**', line)
        if line != original_line:
            changes_made += 1
            original_line = line
        
        # Fix broken bullet patterns: **- item
        line = re.sub(r'^\*\*-\s*([^*]+)', r'- **\1**', line)
        if line != original_line:
            changes_made += 1
            original_line = line
        
        # Fix missing closing asterisks at end of lines
        # Pattern: - **text*
        line = re.sub(r'-\s*\*\*([^*]+)\*\s*$', r'- **\1**', line)
        if line != original_line:
            changes_made += 1
            original_line = line
        
        # Fix standalone asterisks patterns
        line = re.sub(r'^\*\*$', '', line)
        if line != original_line:
            changes_made += 1
            original_line = line
        
        # Fix patterns like: ****text:****
        line = re.sub(r'\*\*\*\*([^*:]+):\*\*\*\*', r'**\1:**', line)
        if line != original_line:
            changes_made += 1
            original_line = line
        
        # Fix HTML/markdown mixing issues in arena cards
        # Remove stray ** markers that are breaking formatting
        if '<div class="arena-card"' in line:
            line = re.sub(r'\*\*\*\*', '**', line)
            if line != original_line:
                changes_made += 1
                original_line = line
        
        # Fix malformed bullets that should be headers
        if re.match(r'-\s*\*\*([^*:]+):\*\*\s*$', line):
            content_match = re.match(r'-\s*\*\*([^*:]+):\*\*\s*$', line)
            if content_match:
                line = f"**{content_match.group(1)}:**"
                changes_made += 1
        
        # Clean up consecutive asterisks
        line = re.sub(r'\*{6,}', '**', line)
        if line != original_line:
            changes_made += 1
            original_line = line
        
        # Fix broken code blocks
        line = re.sub(r'\*\*```', '```', line)
        line = re.sub(r'```\*\*', '```', line)
        if line != original_line:
            changes_made += 1
        
        fixed_lines.append(line)
    
    return '\n'.join(fixed_lines), changes_made

def main():
    """Process all markdown files in the docs directory."""
    docs_dir = Path("docs")
    total_changes = 0
    files_processed = 0
    
    print("🔧 Final markdown formatting fixes...")
    
    for md_file in docs_dir.rglob("*.md"):
        try:
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            fixed_content, changes = fix_markdown_issues(content, str(md_file))
            
            if changes > 0:
                with open(md_file, 'w', encoding='utf-8') as f:
                    f.write(fixed_content)
                
                print(f"  ✅ {md_file}: {changes} fixes")
                total_changes += changes
                files_processed += 1
            
        except Exception as e:
            print(f"  ❌ Error processing {md_file}: {e}")
    
    print(f"\n🎉 Final fix complete!")
    print(f"   📁 Files processed: {files_processed}")
    print(f"   🔧 Total fixes: {total_changes}")

if __name__ == "__main__":
    main()