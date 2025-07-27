#!/usr/bin/env python3
import os
import re

def fix_all_formatting_issues(content):
    """Fix all major formatting issues in markdown files."""
    
    # Fix info/warning/tip blocks with split bold text
    content = re.sub(
        r'!!! (info|warning|tip|quote|danger|success) "([^"]+)"\n\s+\*\*([^:]+):\s*\n\s*\*\*',
        r'!!! \1 "\2"\n    **\3:**',
        content,
        flags=re.MULTILINE
    )
    
    # Fix bold text split across lines ending with asterisks
    content = re.sub(
        r'\*\*([^*\n]+)\*\s*\n\s*\*\*',
        r'**\1**',
        content,
        flags=re.MULTILINE
    )
    
    # Fix bold text with colons split across lines
    content = re.sub(
        r'\*\*([^*\n]+):\s*\n\s*\*\*',
        r'**\1:**',
        content,
        flags=re.MULTILINE
    )
    
    # Fix lists that have items concatenated on one line
    # Pattern: "- item1- item2" -> "- item1\n- item2"
    content = re.sub(
        r'(\s*)([-*]\s+[^-\n]+)([-*]\s+)',
        r'\1\2\n\1\3',
        content,
        flags=re.MULTILINE
    )
    
    # Fix numbered lists similarly
    content = re.sub(
        r'(\s*)(\d+\.\s+[^-\n]+)(\d+\.\s+)',
        r'\1\2\n\1\3',
        content,
        flags=re.MULTILINE
    )
    
    # Fix cases where there's text with trailing asterisks on separate lines
    content = re.sub(
        r'([^*\n]+)\*\s*\n\s*\*([^*\n]+)',
        r'\1*\2',
        content,
        flags=re.MULTILINE
    )
    
    # Fix arena card lists that need blank lines after headings/bold text
    lines = content.split('\n')
    fixed_lines = []
    i = 0
    in_arena_card = False
    
    while i < len(lines):
        line = lines[i].strip()
        
        # Check if we're entering/exiting an arena card
        if 'class="arena-card"' in line:
            in_arena_card = True
        elif '</div>' in line and in_arena_card:
            in_arena_card = False
        
        # Add the current line
        fixed_lines.append(lines[i])
        
        # If we're in an arena card and this line ends with a colon or bold text
        # and the next line starts with a list marker, add a blank line
        if in_arena_card and i + 1 < len(lines):
            next_line = lines[i + 1].strip()
            if (line.endswith(':') or line.endswith('**')) and \
               (next_line.startswith('-') or next_line.startswith('*') or 
                re.match(r'^\d+\.', next_line)):
                # Check if there's not already a blank line
                if next_line != '':
                    fixed_lines.append('')
        
        i += 1
    
    content = '\n'.join(fixed_lines)
    
    # Fix cases where multiple items are on one line with just a space
    # Pattern: "- Item 1 - Item 2" should be "- Item 1\n- Item 2"
    content = re.sub(
        r'^(\s*[-*])\s+([^-\n]+)\s+([-*])\s+',
        r'\1 \2\n\1 ',
        content,
        flags=re.MULTILINE
    )
    
    # Remove "No newline at end of file" artifacts
    content = re.sub(r'\n*No newline at end of file$', '', content)
    
    return content

def process_file(filepath):
    """Process a single file to fix formatting."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    fixed_content = fix_all_formatting_issues(content)
    
    if fixed_content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(fixed_content)
        return True
    return False

def main():
    docs_dir = '/home/inocult/projects/studio3-docs/docs'
    fixed_files = []
    
    for root, dirs, files in os.walk(docs_dir):
        for file in files:
            if file.endswith('.md'):
                filepath = os.path.join(root, file)
                if process_file(filepath):
                    fixed_files.append(filepath)
                    print(f"Fixed: {filepath}")
    
    print(f"\nTotal files fixed: {len(fixed_files)}")

if __name__ == "__main__":
    main()