#!/usr/bin/env python3
import os
import re

def fix_colon_lists(content):
    """Fix lists that appear after text ending with colon."""
    # Pattern to match text ending with colon followed immediately by a list item
    # This handles both bold text and regular text
    patterns = [
        # Bold text ending with colon followed by list
        (r'(\*\*[^*]+:\*\*)(\s*)([-*])', r'\1\n\n\3'),
        # Regular text ending with colon followed by list  
        (r'([^*\n]+:)(\s*)([-*])', r'\1\n\n\3'),
        # Handle cases where there's already one newline but we need two
        (r'(\*\*[^*]+:\*\*)\n([-*])', r'\1\n\n\2'),
        (r'([^*\n]+:)\n([-*])', r'\1\n\n\2')
    ]
    
    fixed_content = content
    for pattern, replacement in patterns:
        fixed_content = re.sub(pattern, replacement, fixed_content, flags=re.MULTILINE)
    
    return fixed_content

def process_file(filepath):
    """Process a single file to fix formatting."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Only process if file contains arena-card
    if 'arena-card' not in content:
        return False
    
    original_content = content
    fixed_content = fix_colon_lists(content)
    
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