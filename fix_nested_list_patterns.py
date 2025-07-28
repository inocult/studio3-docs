#!/usr/bin/env python3
"""
Fix nested list patterns and malformed bold text issues
"""

import os
import re
import glob
from pathlib import Path

def fix_nested_patterns(content):
    """Fix nested list patterns and bold formatting issues"""
    fixes_count = 0
    lines = content.split('\n')
    fixed_lines = []
    
    i = 0
    while i < len(lines):
        line = lines[i]
        original_line = line
        
        # Pattern 1: **text:** 1.**text** → **text:**\n\n1. **text**
        # Match bold text ending with colon followed by numbered list
        match1 = re.match(r'^(\s*)(\*\*[^*]+:\*\*)\s*(\d+)\.\s*\*\*(.+)$', line)
        if match1:
            indent = match1.group(1)
            header = match1.group(2)
            number = match1.group(3)
            rest = match1.group(4)
            
            fixed_lines.append(f"{indent}{header}")
            fixed_lines.append("")  # Add blank line
            fixed_lines.append(f"{indent}{number}. **{rest}")
            fixes_count += 1
            i += 1
            continue
        
        # Pattern 2: Fix missing closing ** in nested bullet lists
        # Like: - **text**: description** → - **text**: description
        match2 = re.match(r'^(\s*-\s*\*\*[^*]+:\*\*)\s*([^*]+)\*\*\s*$', line)
        if match2:
            prefix = match2.group(1)
            desc = match2.group(2)
            fixed_lines.append(f"{prefix} {desc}")
            fixes_count += 1
            i += 1
            continue
        
        # Pattern 3: Multiple list items on same line with dash prefix
        # Like: - **Item1** - Item2 - Item3
        if line.strip().startswith('-') and line.count(' - ') >= 1:
            # Split properly while preserving bold formatting
            parts = re.split(r'\s+-\s+', line)
            if len(parts) > 1:
                # First item
                fixed_lines.append(parts[0])
                # Rest of items
                for j in range(1, len(parts)):
                    if parts[j].strip():
                        fixed_lines.append(f"- {parts[j].strip()}")
                fixes_count += 1
                i += 1
                continue
        
        # Pattern 4: Fix lines with structure like "2. **text**" at the start
        # that should be "2. **text**"
        match4 = re.match(r'^(\s*)(\d+)\.\s*\*\*\s*(.+)$', line)
        if match4 and not line.endswith('**'):
            indent = match4.group(1)
            number = match4.group(2)
            text = match4.group(3)
            # Check if text already has ** somewhere
            if '**' in text:
                # Just add the line as is
                fixed_lines.append(line)
            else:
                # Add closing **
                fixed_lines.append(f"{indent}{number}. **{text}**")
                fixes_count += 1
            i += 1
            continue
        
        # Pattern 5: Fix !!! info blocks with malformed content
        if line.strip().startswith('!!! info'):
            fixed_lines.append(line)
            i += 1
            # Process the content of the info block
            while i < len(lines) and (lines[i].startswith('    ') or lines[i].strip() == ''):
                info_line = lines[i]
                # Fix patterns within info blocks
                # Pattern: - **text**: description** → - **text**: description
                info_match = re.match(r'^(\s+)-\s*\*\*([^*]+)\*\*\s*:\s*([^*]+)\*\*\s*$', info_line)
                if info_match:
                    indent = info_match.group(1)
                    bold_text = info_match.group(2)
                    desc = info_match.group(3)
                    fixed_lines.append(f"{indent}- **{bold_text}**: {desc}")
                    fixes_count += 1
                else:
                    fixed_lines.append(info_line)
                i += 1
            continue
        
        # Default: add line as-is
        fixed_lines.append(line)
        i += 1
    
    return '\n'.join(fixed_lines), fixes_count

def process_file(file_path):
    """Process a single markdown file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Apply fixes
        fixed_content, fixes = fix_nested_patterns(content)
        
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
    
    print("🔧 Fixing nested list patterns and formatting issues...")
    print("Patterns being fixed:")
    print("  - **text:** 1.**text** → proper formatting")
    print("  - Missing closing ** in nested lists")
    print("  - Multiple list items on same line")
    print("  - Info block formatting issues")
    print()
    
    # Process all markdown files
    for md_file in sorted(docs_dir.rglob("*.md")):
        fixes = process_file(md_file)
        if fixes > 0:
            total_fixes += fixes
            files_processed += 1
    
    print(f"\n🎉 Nested pattern fix complete!")
    print(f"   📁 Files updated: {files_processed}")
    print(f"   🔧 Total fixes: {total_fixes}")

if __name__ == "__main__":
    main()