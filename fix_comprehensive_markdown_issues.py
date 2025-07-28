#!/usr/bin/env python3
"""
Fix comprehensive markdown issues across all files
"""

import os
import re
import glob
from pathlib import Path

def fix_markdown_file(file_path):
    """Fix common markdown issues in a file"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # Fix space before colon in bold text
    content = re.sub(r'(\*\*[^*]+\*\*)\s+:', r'\1:', content)
    
    # Fix space after opening bold marker in lists
    content = re.sub(r'^([-*]\s+)\*\*\s+', r'\1**', content, flags=re.MULTILINE)
    
    # Fix missing space after colon (but not in URLs, times, or special patterns)
    def fix_colon_space(match):
        full_match = match.group(0)
        before = match.group(1)
        after = match.group(2)
        
        # Skip URLs, times, emoji patterns
        if any(pattern in before for pattern in ['http', 'https', 'mailto', 'ftp']):
            return full_match
        if re.match(r'^\d+$', after):  # Time pattern like 10:30
            return full_match
        if re.match(r'^[a-zA-Z]+$', after) and len(after) <= 10:  # Emoji pattern
            return full_match
            
        return f"{before}: {after}"
    
    content = re.sub(r'([^:\s]):([\w])', fix_colon_space, content)
    
    # Fix tables without blank line before
    lines = content.split('\n')
    fixed_lines = []
    
    for i, line in enumerate(lines):
        # Add blank line before table if needed
        if '|' in line and line.count('|') >= 3 and i > 0:
            prev_line = lines[i-1] if i > 0 else ''
            if prev_line.strip() and not prev_line.strip().startswith('|') and not prev_line.strip().endswith(':'):
                fixed_lines.append('')
        
        fixed_lines.append(line)
    
    content = '\n'.join(fixed_lines)
    
    # Fix headers without blank line before
    lines = content.split('\n')
    fixed_lines = []
    
    for i, line in enumerate(lines):
        # Add blank line before header if needed
        if re.match(r'^#{1,6}\s+', line) and i > 0:
            prev_line = lines[i-1] if i > 0 else ''
            if prev_line.strip() and not prev_line.startswith('#'):
                fixed_lines.append('')
        
        fixed_lines.append(line)
    
    content = '\n'.join(fixed_lines)
    
    # Fix patterns like "** text" at start of lines
    content = re.sub(r'^(\s*)\*\*\s+', r'\1**', content, flags=re.MULTILINE)
    
    # Fix missing line breaks after bold headers with colons
    content = re.sub(r'(\*\*[^*]+:\*\*)(\n)([^\n])', r'\1\n\n\3', content)
    
    # Fix numbered lists with improper indentation
    lines = content.split('\n')
    fixed_lines = []
    in_numbered_list = False
    
    for line in lines:
        if re.match(r'^\d+\.\s+', line):
            in_numbered_list = True
            fixed_lines.append(line)
        elif in_numbered_list and line.strip() and not line.startswith(' '):
            # Line after numbered list should be indented or separated
            if not re.match(r'^\d+\.\s+', line) and not line.startswith('#'):
                in_numbered_list = False
            fixed_lines.append(line)
        else:
            if line.strip() == '':
                in_numbered_list = False
            fixed_lines.append(line)
    
    content = '\n'.join(fixed_lines)
    
    # Fix "- ** pattern" to "- **pattern"
    content = re.sub(r'^([-*]\s+)\*\*\s+', r'\1**', content, flags=re.MULTILINE)
    
    # Fix multiple consecutive blank lines
    content = re.sub(r'\n{4,}', '\n\n\n', content)
    
    # Ensure file ends with newline
    if content and not content.endswith('\n'):
        content += '\n'
    
    # Only write if changed
    if content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    
    return False

def main():
    """Process all markdown files"""
    fixed_count = 0
    total_count = 0
    
    md_files = glob.glob('docs/**/*.md', recursive=True)
    
    print(f"🔧 Fixing markdown issues in {len(md_files)} files...")
    
    for file_path in sorted(md_files):
        total_count += 1
        if fix_markdown_file(file_path):
            fixed_count += 1
            print(f"  ✅ Fixed: {file_path}")
    
    print(f"\n✨ Complete! Fixed {fixed_count}/{total_count} files.")

if __name__ == "__main__":
    main()