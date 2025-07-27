#!/usr/bin/env python3
import os
import re

def fix_formatting_issues(content):
    """Fix various markdown formatting issues."""
    
    # Fix info blocks where content is on wrong lines
    content = re.sub(
        r'(\!\!\! \w+ "[^"]+"\n)(\s+)\*\*([^:]+):\n(\s+)\*\*([^*]+)\*\*',
        r'\1\2**\3:** \5',
        content,
        flags=re.MULTILINE
    )
    
    # Fix lists that appear after text ending with colon (without bold)
    content = re.sub(
        r'([^*\n][^*\n]+:)\s*\n\s*([-*]\s)',
        r'\1\n\n\2',
        content,
        flags=re.MULTILINE
    )
    
    # Fix cases where there's text between ** markers on separate lines in lists
    content = re.sub(
        r'(\s*)([-*]\s+)(.+)- (.+)- (.+)- (.+)',
        lambda m: m.group(1) + m.group(2) + m.group(3) + '\n' + m.group(1) + '- ' + m.group(4) + '\n' + m.group(1) + '- ' + m.group(5) + '\n' + m.group(1) + '- ' + m.group(6),
        content,
        flags=re.MULTILINE
    )
    
    # Fix double asterisk formatting split across lines
    content = re.sub(
        r'\*\*([^*\n]+):\n\n\*\*\s*',
        r'**\1:** ',
        content,
        flags=re.MULTILINE
    )
    
    # Fix cases where list items are concatenated on one line
    # Look for patterns like "- item1- item2- item3"
    content = re.sub(
        r'(\s*)([-*]\s+[^-\n]+)([-*]\s+)',
        r'\1\2\n\1\3',
        content,
        flags=re.MULTILINE
    )
    
    return content

def process_file(filepath):
    """Process a single file to fix formatting."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    fixed_content = fix_formatting_issues(content)
    
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