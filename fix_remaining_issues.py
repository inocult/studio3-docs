#!/usr/bin/env python3
"""
Script to fix remaining common markdown issues
"""

import os
import re
import glob
from pathlib import Path

def fix_remaining_issues(content):
    """Fix remaining common markdown formatting issues"""
    
    lines = content.split('\n')
    result_lines = []
    prev_line = ""
    
    for i, line in enumerate(lines):
        original_line = line
        
        # Fix missing spaces after colons in patterns like "**Text:**Content"
        line = re.sub(r'(\*\*[^*]+:\*\*)([A-Z][^|*\n])', r'\1 \2', line)
        
        # Fix patterns like "**Text:Content" -> "**Text:** Content"
        line = re.sub(r'(\*\*[^*]+):([A-Z][^*\n])', r'\1:** \2', line)
        
        # Fix table headers with double asterisks like |**Text** | -> | **Text** |
        line = re.sub(r'\|\*\*([^*|]+)\*\*\s*\|', r'| **\1** |', line)
        
        # Fix numbered lists with unclosed bolds like "1. **Text** (40%)**"
        line = re.sub(r'^(\d+\.\s+\*\*[^*]+\*\*[^*]*)\*\*([^*]*)$', r'\1\2', line)
        
        # Add blank lines before headers if needed
        stripped = line.strip()
        prev_stripped = prev_line.strip()
        
        if (stripped.startswith('##') and prev_stripped and 
            not prev_stripped.startswith('#') and 
            not prev_stripped == ''):
            result_lines.append('')
        
        # Add blank lines before lists if needed
        if (re.match(r'^[-*]\s+\*\*[^*]+', stripped) and 
            prev_stripped and 
            not prev_stripped.startswith('-') and 
            not prev_stripped.startswith('*') and
            not prev_stripped == ''):
            result_lines.append('')
        
        result_lines.append(line)
        prev_line = original_line
    
    return '\n'.join(result_lines)

def fix_specific_arena_card_issues(content):
    """Fix arena-card specific formatting issues"""
    
    # Fix arena-cards that have HTML content but still have markdown="1" 
    lines = content.split('\n')
    result_lines = []
    in_arena_card = False
    arena_card_start = -1
    has_html_content = False
    
    for i, line in enumerate(lines):
        if '<div class="arena-card" markdown="1">' in line:
            in_arena_card = True
            arena_card_start = i
            has_html_content = False
        elif in_arena_card:
            # Check for HTML content
            if re.search(r'<[^>]+>', line) and not line.strip().startswith('```'):
                has_html_content = True
            elif '</div>' in line and in_arena_card:
                # End of arena-card, fix if needed
                if has_html_content and arena_card_start >= 0:
                    # Remove markdown="1" from arena-card with HTML content
                    result_lines[arena_card_start] = result_lines[arena_card_start].replace(' markdown="1"', '')
                in_arena_card = False
                arena_card_start = -1
                has_html_content = False
        
        result_lines.append(line)
    
    return '\n'.join(result_lines)

def fix_file(filepath):
    """Fix remaining issues in a single file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            original_content = f.read()
        
        fixed_content = fix_remaining_issues(original_content)
        fixed_content = fix_specific_arena_card_issues(fixed_content)
        
        if fixed_content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(fixed_content)
            print(f"Fixed: {filepath}")
            return True
        else:
            print(f"No changes: {filepath}")
            return False
            
    except Exception as e:
        print(f"Error processing {filepath}: {str(e)}")
        return False

def main():
    """Fix remaining issues in all markdown files"""
    docs_dir = 'docs'
    md_files = glob.glob(os.path.join(docs_dir, '**/*.md'), recursive=True)
    
    print(f"Processing {len(md_files)} markdown files for remaining issues...")
    
    fixed_count = 0
    for filepath in sorted(md_files):
        if fix_file(filepath):
            fixed_count += 1
    
    print(f"\nCompleted: {fixed_count} files modified")

if __name__ == "__main__":
    main()