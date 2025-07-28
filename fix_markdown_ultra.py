#!/usr/bin/env python3
"""
Ultra markdown fixer - fixes all common markdown formatting issues
"""

import os
import re
import sys
import glob

def fix_markdown_file(filepath):
    """Fix markdown formatting issues in a single file"""
    
    print(f"Fixing {filepath}...")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        lines = content.split('\n')
    
    fixed_lines = []
    in_code_block = False
    in_arena_card = False
    changes_made = 0
    
    for i, line in enumerate(lines):
        original_line = line
        
        # Track code blocks to skip processing
        if '```' in line:
            in_code_block = not in_code_block
        
        # Track arena cards
        if '<div class="arena-card"' in line:
            in_arena_card = True
            # Fix missing markdown="1"
            if 'markdown="1"' not in line:
                line = line.replace('>', ' markdown="1">')
                changes_made += 1
                
        elif '<div class="grid' in line and 'markdown="1"' not in line:
            line = line.replace('>', ' markdown="1">')
            changes_made += 1
            
        elif '</div>' in line and in_arena_card:
            in_arena_card = False
        
        # Don't process lines in code blocks
        if not in_code_block:
            # Fix **text** : pattern (space before colon)
            line = re.sub(r'(\*\*[^*]+\*\*)\s+:', r'\1:', line)
            
            # Fix missing space after colon (but not in URLs, times, emoji)
            if ':' in line:
                # Complex regex to add space after colon when needed
                def fix_colon(match):
                    prefix = match.group(1)
                    suffix = match.group(2)
                    # Check if it's a special case
                    if re.match(r'^(\/\/|[0-9]|[a-zA-Z]:|\w+:|\)|\]|\})', suffix):
                        return match.group(0)
                    return prefix + ': ' + suffix
                
                line = re.sub(r'(:)([^\s])', fix_colon, line)
            
            # Fix - ** text pattern (space after opening bold)
            line = re.sub(r'^(\s*[-*]\s+)\*\*\s+', r'\1**', line)
            
            # Fix text** pattern (add opening bold if missing)
            if re.search(r'[^\*]\*\*$', line) and line.count('**') % 2 != 0:
                # Find where the bold should start (usually after a space or punctuation)
                line = re.sub(r'(\s|^)([A-Z][^\*]+)\*\*$', r'\1**\2**', line)
                
            # Fix **text**text** pattern (add space between bold sections)
            line = re.sub(r'(\*\*[^*]+\*\*)([^\s*:,;.!?)\]}>])([^*]*\*\*)', r'\1 \2\3', line)
            
            # Fix double dashes at line start
            line = re.sub(r'^--\s+', '- ', line)
            
            # Fix $STUDIO to $SIGNAL
            line = line.replace('$STUDIO', '$SIGNAL')
            
            # Fix list markers without space
            line = re.sub(r'^(\s*)([-*])(\w)', r'\1\2 \3', line)
            line = re.sub(r'^(\s*)(\d+\.)(\w)', r'\1\2 \3', line)
            
            # Fix orphaned bold markers
            if line.strip() in ['**', '** ']:
                line = ''
                
            # Fix bold patterns that continue from previous line
            if i > 0 and lines[i-1].rstrip().endswith('**'):
                # Check if this line starts with capital letter (likely continuation)
                if re.match(r'^[A-Z]', line.strip()) and '**' not in line:
                    # Add opening bold
                    line = re.sub(r'^(\s*)([A-Z])', r'\1**\2', line)
                    
            # Fix patterns like **Something: (missing closing bold)
            if re.match(r'^(\s*[-*]\s+)?\*\*[^*]+:(?!\*)', line):
                if '**' not in line[line.index('**')+2:]:
                    # Add closing bold before colon
                    line = re.sub(r'(\*\*[^*]+):', r'\1**:', line)
                    
            # Fix list items with bold and content on same line
            if re.match(r'^(\s*[-*]\s+)\*\*[^*]+\*\*:\s*\w', line):
                # Split into two lines
                match = re.match(r'^(\s*[-*]\s+)(\*\*[^*]+\*\*:)\s*(.+)$', line)
                if match:
                    indent = match.group(1)
                    bold_part = match.group(2)
                    content = match.group(3)
                    line = bold_part
                    # Insert content as next line with proper indentation
                    fixed_lines.append(line)
                    line = '  ' + content  # Standard 2-space indent for continuation
                    changes_made += 1
                    
        if line != original_line:
            changes_made += 1
            
        fixed_lines.append(line)
    
    # Post-process to add blank lines where needed
    final_lines = []
    prev_line = ""
    
    for i, line in enumerate(fixed_lines):
        # Add blank line before headers (unless after another header or at start)
        if line.strip().startswith('#') and prev_line.strip() and not prev_line.strip().startswith('#'):
            if not final_lines or final_lines[-1].strip():
                final_lines.append('')
                changes_made += 1
                
        # Add blank line before tables
        if line.strip().startswith('|') and prev_line.strip() and not prev_line.strip().startswith('|'):
            if not final_lines or final_lines[-1].strip():
                final_lines.append('')
                changes_made += 1
                
        # Add blank line before lists (at indent 0)
        if re.match(r'^[-*]\s+', line) and prev_line.strip() and not re.match(r'^[-*]\s+', prev_line):
            if not final_lines or final_lines[-1].strip():
                final_lines.append('')
                changes_made += 1
                
        final_lines.append(line)
        prev_line = line
    
    # Remove multiple consecutive blank lines
    cleaned_lines = []
    blank_count = 0
    
    for line in final_lines:
        if not line.strip():
            blank_count += 1
            if blank_count <= 2:
                cleaned_lines.append(line)
        else:
            blank_count = 0
            cleaned_lines.append(line)
    
    # Ensure file ends with newline
    if cleaned_lines and cleaned_lines[-1] != '':
        cleaned_lines.append('')
    
    # Write fixed content
    if changes_made > 0:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write('\n'.join(cleaned_lines))
        print(f"  Fixed {changes_made} issues")
        return 1
    else:
        print(f"  No issues found")
        return 0

def main():
    """Main entry point"""
    
    if len(sys.argv) > 1:
        # Single file mode
        files = [sys.argv[1]]
    else:
        # Process all markdown files
        files = glob.glob('docs/**/*.md', recursive=True)
    
    total_files_fixed = 0
    
    print("🔧 Ultra Markdown Fixer")
    print(f"Processing {len(files)} files...\n")
    
    for filepath in sorted(files):
        if os.path.exists(filepath):
            if fix_markdown_file(filepath) > 0:
                total_files_fixed += 1
    
    print(f"\n✅ Fixed {total_files_fixed} files")

if __name__ == "__main__":
    main()