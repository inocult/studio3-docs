#!/usr/bin/env python3
"""
Fix task lists for Material for MkDocs theme by ensuring proper formatting
"""

import os
import re
from pathlib import Path

def fix_material_tasklist(content):
    """Fix task lists to work properly with Material for MkDocs"""
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
        
        # Process content
        if in_arena_card:
            # For headers followed by task lists, ensure proper spacing
            if line.strip().startswith('**') and line.strip().endswith(':**'):
                fixed_lines.append(line)
                # Look ahead to see if next non-empty line is a task list
                j = i + 1
                while j < len(lines) and not lines[j].strip():
                    j += 1
                if j < len(lines) and (lines[j].strip().startswith('- [ ]') or lines[j].strip().startswith('- [x]')):
                    # Ensure we have exactly one blank line before the task list
                    if j == i + 1:
                        fixed_lines.append('')  # Add blank line
                        changes_made += 1
                i += 1
                continue
            
            # Fix task list items - Material needs exact formatting
            if line.strip().startswith(('- [ ]', '- [x]')):
                # Ensure no leading spaces for top-level items in arena cards
                clean_line = line.strip()
                # Ensure exactly one space after dash and proper bracket spacing
                clean_line = re.sub(r'^-\s*\[\s*\]', '- [ ]', clean_line)
                clean_line = re.sub(r'^-\s*\[x\]', '- [x]', clean_line)
                fixed_lines.append(clean_line)
                if clean_line != line:
                    changes_made += 1
                i += 1
                continue
        
        # For task lists outside arena cards, preserve original indentation
        if not in_arena_card and (line.startswith('- [ ]') or line.startswith('- [x]')):
            # Just ensure proper bracket spacing
            clean_line = re.sub(r'-\s*\[\s*\]', '- [ ]', line)
            clean_line = re.sub(r'-\s*\[x\]', '- [x]', clean_line)
            fixed_lines.append(clean_line)
            if clean_line != line:
                changes_made += 1
            i += 1
            continue
        
        # Default: add line as-is
        fixed_lines.append(line)
        i += 1
    
    # Post-process to ensure Material for MkDocs requirements
    final_lines = []
    for i, line in enumerate(fixed_lines):
        # Ensure task lists use proper Material syntax
        if line.strip().startswith(('- [ ]', '- [x]')):
            # Material for MkDocs is picky about task list format
            match = re.match(r'^(\s*)-\s*\[([ x])\]\s*(.*)$', line)
            if match:
                indent = match.group(1)
                check = match.group(2)
                content = match.group(3)
                # Reconstruct with exact format Material expects
                final_lines.append(f"{indent}- [{check}] {content}")
                if line != f"{indent}- [{check}] {content}":
                    changes_made += 1
            else:
                final_lines.append(line)
        else:
            final_lines.append(line)
    
    return '\n'.join(final_lines), changes_made

def add_tasklist_extension_hint(content):
    """Add a comment about task list requirements if not present"""
    if '<!-- tasklist -->' not in content and ('- [ ]' in content or '- [x]' in content):
        # Add hint at top of file
        return f"<!-- tasklist -->\n{content}", 1
    return content, 0

def process_file(file_path):
    """Process a single markdown file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Apply task list fixes
        fixed_content, changes1 = fix_material_tasklist(content)
        
        # Add extension hint if needed
        fixed_content, changes2 = add_tasklist_extension_hint(fixed_content)
        
        total_changes = changes1 + changes2
        
        if total_changes > 0:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(fixed_content)
            print(f"✅ {file_path}: {total_changes} task list fixes")
            return total_changes
        
        return 0
        
    except Exception as e:
        print(f"❌ Error processing {file_path}: {e}")
        return 0

def main():
    """Process all markdown files"""
    docs_dir = Path("docs")
    total_changes = 0
    files_processed = 0
    
    print("🔧 Fixing task lists for Material for MkDocs...")
    print("ℹ️  Ensure pymdownx.tasklist is enabled in mkdocs.yml")
    
    # Check mkdocs.yml for tasklist extension
    mkdocs_path = Path("mkdocs.yml")
    if mkdocs_path.exists():
        with open(mkdocs_path, 'r') as f:
            mkdocs_content = f.read()
            if 'pymdownx.tasklist' not in mkdocs_content:
                print("⚠️  WARNING: pymdownx.tasklist not found in mkdocs.yml")
                print("   Add under markdown_extensions:")
                print("   - pymdownx.tasklist:")
                print("       custom_checkbox: true")
    
    for md_file in docs_dir.rglob("*.md"):
        changes = process_file(md_file)
        if changes > 0:
            total_changes += changes
            files_processed += 1
    
    print(f"\n🎉 Task list formatting complete!")
    print(f"   📁 Files updated: {files_processed}")
    print(f"   🔧 Total fixes: {total_changes}")

if __name__ == "__main__":
    main()