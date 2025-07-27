#!/usr/bin/env python3
import os
import re
import sys

def fix_markdown_patterns(content):
    """Fix various markdown rendering issues."""
    
    # Pattern 1: Fix lines that have bold text followed by extra ** on next line
    # Example:
    # - **Access** **
    # - Anyone can participate
    # Should become:
    # - **Access** - Anyone can participate
    content = re.sub(r'(- \*\*[^*]+\*\*)\s*\*\*\s*\n\s*-\s*([^\n]+)', r'\1 - \2', content)
    
    # Pattern 2: Fix standalone ** on separate lines
    content = re.sub(r'^\s*\*\*\s*$', '', content, flags=re.MULTILINE)
    
    # Pattern 3: Fix broken bold patterns at end of lines
    # **Text** ** -> **Text**
    content = re.sub(r'(\*\*[^*]+\*\*)\s*\*\*\s*$', r'\1', content, flags=re.MULTILINE)
    
    # Pattern 4: Fix double ** at the beginning of lines after a list item
    # **- **Text** -> - **Text**
    content = re.sub(r'^(\s*)\*\*-\s*\*\*([^*]+)\*\*', r'\1- **\2**', content, flags=re.MULTILINE)
    
    # Pattern 5: Fix orphaned * at the end of lines
    # - **Text**
    # * with content -> - **Text** with content
    content = re.sub(r'(- \*\*[^*]+)\*\*\s*\n\s*\*\s+([^\n]+)', r'\1** \2', content)
    
    # Pattern 6: Fix patterns like:
    # - **Team**: 3-5x expansion**
    # Should be: - **Team**: 3-5x expansion
    content = re.sub(r'(- \*\*[^:]+\*\*:)([^*]+)\*\*\s*$', r'\1\2', content, flags=re.MULTILINE)
    
    # Pattern 7: Fix numbered lists with broken bold
    # 1. **Text** - Description**
    # Should be: 1. **Text** - Description
    content = re.sub(r'(\d+\.\s+\*\*[^*]+\*\*[^*]+)\*\*\s*$', r'\1', content, flags=re.MULTILINE)
    
    # Pattern 8: Clean up multiple consecutive asterisks
    content = re.sub(r'\*{3,}', '**', content)
    
    # Pattern 9: Fix lines that end with ****
    content = re.sub(r'\*{4}\s*$', '', content, flags=re.MULTILINE)
    
    # Pattern 10: Fix **Phase**: text** patterns
    content = re.sub(r'\*\*([^*:]+)\*\*:\s*([^*\n]+)\*\*', r'**\1**: \2', content)
    
    return content

def process_file(filepath):
    """Process a single markdown file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        fixed_content = fix_markdown_patterns(content)
        
        if fixed_content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(fixed_content)
            return True
        return False
    except Exception as e:
        print(f"Error processing {filepath}: {e}")
        return False

def main():
    docs_dir = '/home/inocult/projects/studio3-docs/docs'
    
    fixed_count = 0
    total_files = 0
    
    for root, dirs, files in os.walk(docs_dir):
        for file in files:
            if file.endswith('.md'):
                filepath = os.path.join(root, file)
                total_files += 1
                
                if process_file(filepath):
                    fixed_count += 1
                    print(f"Fixed: {filepath}")
    
    print(f"\nProcessed {total_files} files, fixed {fixed_count} files.")

if __name__ == "__main__":
    main()