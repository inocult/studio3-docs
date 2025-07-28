#!/usr/bin/env python3
"""
Fix checklist formatting in arena cards by ensuring proper indentation and spacing
"""

import os
import re
from pathlib import Path

def fix_checklist_formatting(content):
    """Fix checklist items to render properly in arena cards"""
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
        elif '</div>' in line and in_arena_card:
            arena_depth -= 1
            if arena_depth == 0:
                in_arena_card = False
        
        # Inside arena card
        if in_arena_card:
            # Fix patterns where checklist header and items might not have proper spacing
            # Pattern: **Day 1:** followed by checklist items
            if re.match(r'^\*\*[^*]+:\*\*\s*$', line.strip()) and i + 1 < len(lines):
                # This is a bold header, check if next lines are checklist items
                fixed_lines.append(line)
                # Add a blank line after the header if next line is a checklist
                next_line = lines[i + 1].strip() if i + 1 < len(lines) else ""
                if next_line.startswith('- [ ]') or next_line.startswith('- [x]'):
                    fixed_lines.append('')  # Add blank line for better rendering
                    changes_made += 1
                i += 1
                continue
                
            # Ensure checklist items have proper format
            # MkDocs/Material needs specific formatting for task lists
            if re.match(r'^-\s*\[\s*\]', line.strip()) or re.match(r'^-\s*\[x\]', line.strip()):
                # Ensure proper spacing: "- [ ]" not "-[ ]" or "- []"
                clean_line = re.sub(r'^-\s*\[\s*\]', '- [ ]', line.strip())
                clean_line = re.sub(r'^-\s*\[x\]', '- [x]', clean_line)
                
                # Ensure consistent indentation (no extra spaces at start)
                fixed_lines.append(clean_line)
                if clean_line != line.strip():
                    changes_made += 1
                i += 1
                continue
        
        # Default: add line as-is
        fixed_lines.append(line)
        i += 1
    
    # Additional pass to ensure task lists are properly formatted
    final_lines = []
    for i, line in enumerate(fixed_lines):
        if line.strip().startswith('- [ ]') or line.strip().startswith('- [x]'):
            # Ensure there's content after the checkbox
            match = re.match(r'^(-\s*\[[x\s]*\])\s*(.*)$', line.strip())
            if match and match.group(2):
                # Properly format: "- [ ] content"
                final_lines.append(f"{match.group(1)} {match.group(2).strip()}")
                if line != f"{match.group(1)} {match.group(2).strip()}":
                    changes_made += 1
            else:
                final_lines.append(line)
        else:
            final_lines.append(line)
    
    return '\n'.join(final_lines), changes_made

def process_file(file_path):
    """Process a single markdown file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Apply checklist formatting fixes
        fixed_content, changes = fix_checklist_formatting(content)
        
        if changes > 0:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(fixed_content)
            print(f"✅ {file_path}: {changes} checklist formatting fixes")
            return changes
        
        return 0
        
    except Exception as e:
        print(f"❌ Error processing {file_path}: {e}")
        return 0

def main():
    """Process all markdown files"""
    docs_dir = Path("docs")
    total_changes = 0
    files_processed = 0
    
    print("🔧 Fixing checklist formatting in arena cards...")
    
    # Process specific file first for testing
    if Path("docs/quickstart/get-started.md").exists():
        changes = process_file("docs/quickstart/get-started.md")
        if changes > 0:
            total_changes += changes
            files_processed += 1
    
    # Then process all other files
    for md_file in docs_dir.rglob("*.md"):
        if str(md_file) != "docs/quickstart/get-started.md":  # Skip already processed
            changes = process_file(md_file)
            if changes > 0:
                total_changes += changes
                files_processed += 1
    
    print(f"\n🎉 Checklist formatting complete!")
    print(f"   📁 Files updated: {files_processed}")
    print(f"   🔧 Total fixes: {total_changes}")

if __name__ == "__main__":
    main()