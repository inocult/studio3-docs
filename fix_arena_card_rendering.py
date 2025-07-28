#!/usr/bin/env python3
"""
Fix arena-card rendering issues by ensuring proper formatting and line breaks
"""

import os
import re
from pathlib import Path

def fix_arena_card_rendering(content):
    """Fix all arena-card rendering issues comprehensively"""
    lines = content.split('\n')
    fixed_lines = []
    in_arena_card = False
    arena_depth = 0
    changes_made = 0
    
    i = 0
    while i < len(lines):
        line = lines[i]
        
        # Track arena-card state
        if '<div class="arena-card"' in line:
            in_arena_card = True
            arena_depth += 1
            fixed_lines.append(line)
            i += 1
            continue
            
        elif '</div>' in line and in_arena_card:
            arena_depth -= 1
            if arena_depth == 0:
                in_arena_card = False
            fixed_lines.append(line)
            i += 1
            continue
        
        # Process arena-card content
        if in_arena_card and line.strip():
            # Fix patterns where list items run together on same line
            
            # Pattern 1: "**Header:** - item1 - item2 - item3"
            if re.match(r'^\*\*[^*]+:\*\*\s*-\s*', line):
                parts = line.split(' - ')
                if len(parts) > 1:
                    # First part is the header
                    fixed_lines.append(parts[0].rstrip())
                    # Rest are list items
                    for j in range(1, len(parts)):
                        if parts[j].strip():
                            fixed_lines.append(f"- {parts[j].strip()}")
                    changes_made += 1
                    i += 1
                    continue
            
            # Pattern 2: Running bullet list "- item1 - item2 - item3"
            elif line.startswith('-') and line.count(' - ') >= 1:
                # Split carefully to preserve items with dashes in content
                items = re.split(r'\s+-\s+', line)
                if len(items) > 1:
                    for item in items:
                        clean_item = item.strip()
                        if clean_item:
                            if not clean_item.startswith('-'):
                                clean_item = f"- {clean_item}"
                            fixed_lines.append(clean_item)
                    changes_made += 1
                    i += 1
                    continue
            
            # Pattern 3: Bold sections without proper spacing
            # "**If you have:** - item1"
            if ':**' in line and ' - ' in line:
                # Split on the first ' - ' after the bold section
                match = re.match(r'^(\*\*[^*]+:\*\*)\s*-\s*(.+)$', line)
                if match:
                    fixed_lines.append(match.group(1))
                    # Handle the rest which might have more items
                    rest = f"- {match.group(2)}"
                    if ' - ' in rest:
                        items = rest.split(' - ')
                        for item in items:
                            if item.strip():
                                if not item.strip().startswith('-'):
                                    fixed_lines.append(f"- {item.strip()}")
                                else:
                                    fixed_lines.append(item.strip())
                    else:
                        fixed_lines.append(rest)
                    changes_made += 1
                    i += 1
                    continue
            
            # Pattern 4: Numbered lists running together "1. item1 2. item2 3. item3"
            if re.search(r'\d+\.\s+[^0-9]+\s+\d+\.\s+', line):
                # Split on numbered patterns
                parts = re.split(r'(\d+\.\s+)', line)
                current_item = ""
                for part in parts:
                    if re.match(r'\d+\.\s+$', part):
                        if current_item:
                            fixed_lines.append(current_item.strip())
                        current_item = part
                    else:
                        current_item += part
                if current_item:
                    fixed_lines.append(current_item.strip())
                changes_made += 1
                i += 1
                continue
            
            # Pattern 5: Fix checklist items on same line
            if line.count('[ ]') > 1:
                # Handle patterns like "Day 1: - [ ] item1 - [ ] item2"
                if ':' in line:
                    prefix, rest = line.split(':', 1)
                    fixed_lines.append(f"{prefix}:")
                    items = re.split(r'(\s*-\s*\[\s*\][^-]+)', rest)
                    for item in items:
                        if '[ ]' in item and item.strip():
                            clean_item = item.strip()
                            if not clean_item.startswith('-'):
                                clean_item = f"- {clean_item}"
                            fixed_lines.append(clean_item)
                else:
                    # No prefix, just split items
                    items = re.split(r'(\s*-\s*\[\s*\][^-]+)', line)
                    for item in items:
                        if '[ ]' in item and item.strip():
                            clean_item = item.strip()
                            if not clean_item.startswith('-'):
                                clean_item = f"- {clean_item}"
                            fixed_lines.append(clean_item)
                changes_made += 1
                i += 1
                continue
            
            # Pattern 6: Fix inline content after numbered items
            # "1. The Arena System - How public building works"
            if re.match(r'^\d+\.\s+\*\*[^*]+\*\*\s*-\s*', line):
                match = re.match(r'^(\d+\.\s+\*\*[^*]+\*\*)\s*-\s*(.+)$', line)
                if match:
                    fixed_lines.append(match.group(1))
                    fixed_lines.append(f"   - {match.group(2)}")
                    changes_made += 1
                    i += 1
                    continue
            
            # Pattern 7: Ensure spacing after bold headers
            if line.strip().endswith(':**') and i + 1 < len(lines):
                next_line = lines[i + 1].strip()
                if next_line and not next_line.startswith(('-', '*', '#', '1.', '2.', '3.')):
                    fixed_lines.append(line)
                    fixed_lines.append('')  # Add blank line
                    changes_made += 1
                    i += 1
                    continue
                    
        # Add the line as-is if no patterns matched
        fixed_lines.append(line)
        i += 1
    
    return '\n'.join(fixed_lines), changes_made

def process_file(file_path):
    """Process a single markdown file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Apply rendering fixes
        fixed_content, changes = fix_arena_card_rendering(content)
        
        # Apply additional clean-up passes
        if changes > 0:
            # Second pass to catch any remaining issues
            fixed_content, additional_changes = fix_arena_card_rendering(fixed_content)
            changes += additional_changes
        
        if changes > 0:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(fixed_content)
            print(f"✅ {file_path}: {changes} rendering fixes applied")
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
    
    print("🔧 Fixing arena-card rendering issues across all documentation...")
    
    for md_file in docs_dir.rglob("*.md"):
        changes = process_file(md_file)
        if changes > 0:
            total_changes += changes
            files_processed += 1
    
    print(f"\n🎉 Arena-card rendering fixes complete!")
    print(f"   📁 Files updated: {files_processed}")
    print(f"   🔧 Total fixes: {total_changes}")

if __name__ == "__main__":
    main()