#!/usr/bin/env python3
"""
Specialized Arena Card Formatter - Fixes inline list items within arena-card divs
"""

import os
import re
from pathlib import Path

def fix_arena_card_content(content):
    """Fix arena card content formatting issues"""
    lines = content.split('\n')
    fixed_lines = []
    in_arena_card = False
    changes_made = 0
    
    i = 0
    while i < len(lines):
        line = lines[i]
        original_line = line
        
        if '<div class="arena-card"' in line:
            in_arena_card = True
            fixed_lines.append(line)
        elif '</div>' in line and in_arena_card:
            in_arena_card = False
            fixed_lines.append(line)
        elif in_arena_card and line.strip():
            # Process arena card content
            
            # Fix bullet list items running together
            # Pattern: - item1 - item2 - item3 (but not links with dashes)
            if ' - ' in line and not line.strip().startswith('#') and not line.strip().startswith('<'):
                # Count potential bullet items, but be careful with links and descriptions
                potential_items = line.split(' - ')
                
                # Check if this looks like multiple list items vs a single item with description
                if len(potential_items) > 2:
                    # This might be multiple items running together
                    new_items = []
                    for j, item in enumerate(potential_items):
                        clean_item = item.strip()
                        if clean_item:
                            if j == 0 and not clean_item.startswith('-'):
                                # First item might need bullet added
                                if ':' in clean_item or clean_item.endswith(':'):
                                    # This is a header, keep as is
                                    new_items.append(clean_item)
                                else:
                                    new_items.append(f"- {clean_item}")
                            else:
                                # Subsequent items
                                if clean_item.startswith('-'):
                                    new_items.append(clean_item)
                                else:
                                    new_items.append(f"- {clean_item}")
                    
                    # Only split if we have clear multiple items
                    if len(new_items) > 1:
                        fixed_lines.extend(new_items)
                        changes_made += 1
                        i += 1
                        continue
            
            # Fix numbered list items running together
            # Pattern: 1. item1 2. item2 3. item3
            if re.search(r'\d+\.\s+[^0-9]*\d+\.\s+', line):
                # Split on numbered patterns but preserve the content properly
                parts = re.split(r'(?=\d+\.\s+)', line)
                new_numbered_items = []
                
                for part in parts:
                    clean_part = part.strip()
                    if clean_part and re.match(r'^\d+\.', clean_part):
                        new_numbered_items.append(clean_part)
                    elif clean_part:
                        # This is prefix content
                        new_numbered_items.append(clean_part)
                
                if len(new_numbered_items) > 1:
                    fixed_lines.extend(new_numbered_items)
                    changes_made += 1
                    i += 1
                    continue
            
            # Fix checklist items running together
            # Pattern: - [ ] item1 - [ ] item2 - [ ] item3
            if line.count('[ ]') > 1 or line.count('[x]') > 1:
                # Split on checkbox patterns
                checkbox_parts = re.split(r'(\s*-\s*\[[x\s]*\][^-]*?)(?=\s*-\s*\[)', line)
                checkbox_items = []
                
                for part in checkbox_parts:
                    clean_part = part.strip()
                    if clean_part and ('[ ]' in clean_part or '[x]' in clean_part):
                        if not clean_part.startswith('-'):
                            clean_part = f"- {clean_part}"
                        checkbox_items.append(clean_part)
                    elif clean_part and ':' in clean_part:
                        # This might be a prefix like "Day 1:"
                        checkbox_items.append(clean_part)
                
                if len(checkbox_items) > 1:
                    fixed_lines.extend(checkbox_items)
                    changes_made += 1
                    i += 1
                    continue
            
            # No changes needed, add as is
            fixed_lines.append(line)
        else:
            # Not in arena card or empty line
            fixed_lines.append(line)
        
        i += 1
    
    return '\n'.join(fixed_lines), changes_made

def process_file(file_path):
    """Process a single markdown file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        fixed_content, changes = fix_arena_card_content(content)
        
        if changes > 0:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(fixed_content)
            print(f"✅ {file_path}: {changes} arena-card fixes applied")
            return changes
        
        return 0
        
    except Exception as e:
        print(f"❌ Error processing {file_path}: {e}")
        return 0

def main():
    """Process all markdown files in docs directory"""
    docs_dir = Path("docs")
    total_changes = 0
    files_processed = 0
    
    print("🔧 Fixing arena-card formatting across all documentation...")
    
    for md_file in docs_dir.rglob("*.md"):
        changes = process_file(md_file)
        if changes > 0:
            total_changes += changes
            files_processed += 1
    
    print(f"\n🎉 Arena-card formatting complete!")
    print(f"   📁 Files updated: {files_processed}")
    print(f"   🔧 Total fixes: {total_changes}")

if __name__ == "__main__":
    main()