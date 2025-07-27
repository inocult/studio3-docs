#!/usr/bin/env python3
import os
import re

def fix_all_markdown_patterns(content):
    """Fix all markdown rendering issues comprehensively."""
    
    # Pattern 1: Fix incomplete bullet lists where text continues on next line
    # Example: - **Text**\n- ** continuation
    content = re.sub(r'(- \*\*[^*]+\*\*)\s*\n\s*- \*\*\s+([^*\n]+)', r'\1 \2', content)
    
    # Pattern 2: Fix where continuation is on same line with **
    # Example: - **Text** continuation**
    content = re.sub(r'(- \*\*[^*]+\*\*)\s+([^*\n]+)\*\*', r'\1 \2', content)
    
    # Pattern 3: Fix orphaned bullet points with just **
    content = re.sub(r'^- \*\*\s*$', '', content, flags=re.MULTILINE)
    
    # Pattern 4: Fix patterns like **Text:** - content
    # Should be on separate lines
    content = re.sub(r'(\*\*[^:]+:\*\*)\s*-\s*([^\n]+)', r'\1\n- \2', content)
    
    # Pattern 5: Fix SMART-V type patterns where letters are broken
    # - ****M** A should be proper list items
    content = re.sub(r'- \*{4}([A-Z])\*\*\s*([A-Z])', r'- **\1**\n- **\2**', content)
    
    # Pattern 6: Fix Management Strategies that got orphaned
    content = re.sub(r'- \*\*\s*(Management Strategies:)', r'\n**\1**', content)
    
    # Pattern 7: Fix pattern where bold text has asterisk after
    # **Text** * continuation -> **Text** continuation
    content = re.sub(r'(\*\*[^*]+\*\*)\s*\*\s+([^*\n]+)', r'\1 \2', content)
    
    # Pattern 8: Fix Risk-Reward Matrix that appears after text
    content = re.sub(r'([^*]+)\s*(Risk-Reward Matrix:\*\*)', r'\1\n\n**Risk-Reward Matrix:**', content)
    
    # Pattern 9: Fix specific list patterns that are common
    patterns_to_fix = [
        (r'- \*\*Founders\*\*\s*→.*', '- **Founders** → [Senders Guide](../senders-guide/index.md)'),
        (r'\*\*\s*- \*\*Supporters\*\*.*', '    - **Supporters** → [Echoes Guide](../echoes-guide/index.md)'),
        (r'- \*\*Validators\*\*.*', '    - **Validators** → [Anchors Guide](../anchors-guide/index.md)'),
    ]
    
    for pattern, replacement in patterns_to_fix:
        content = re.sub(pattern, replacement, content)
    
    # Pattern 10: Fix numbered lists with broken bold
    content = re.sub(r'(\d+\.\s+\*\*[^*]+\*\*)[:\s]+([^*\n]+)\*\*', r'\1: \2', content)
    
    # Pattern 11: Clean up any quadruple asterisks
    content = re.sub(r'\*{4,}', '**', content)
    
    # Pattern 12: Fix lines ending with orphaned **
    content = re.sub(r'^([^*\n]+)\*\*\s*$', r'\1', content, flags=re.MULTILINE)
    
    # Pattern 13: Fix specific quickstart patterns
    quickstart_fixes = {
        '- **Community wisdom**': '- **Community wisdom** guides venture development',
        '- **Everyone wins**': '- **Everyone wins** when ventures succeed',
        '- **Clarifies concepts**': '- **Clarifies concepts** - Simple language, no jargon',
        '- **Points the way**': '- **Points the way** - Know where to go next'
    }
    
    for old, new in quickstart_fixes.items():
        if old in content:
            content = content.replace(old, new)
    
    # Pattern 14: Fix Studio3 Advantages pattern
    content = re.sub(r'(\*\*Studio3 Advantages:\*\*)\s*-\s*([^\n]+)', r'\1\n- \2', content)
    
    # Pattern 15: Fix For Individuals/Ecosystem/Future patterns
    for pattern in ['For Individuals:', 'For the Ecosystem:', 'For the Future:']:
        content = re.sub(f'(\\*\\*{pattern}\\*\\*)\\s*-\\s*([^\\n]+)', f'\\1\\n- \\2', content)
    
    # Pattern 16: Fix Clear Mechanics pattern
    content = re.sub(r'(\*\*Clear Mechanics:\*\*)\s*-\s*([^\n]+)', r'\1\n- \2', content)
    
    return content

def process_file(filepath):
    """Process a single markdown file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        fixed_content = fix_all_markdown_patterns(content)
        
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
    
    # Process all markdown files
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