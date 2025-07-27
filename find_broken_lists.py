#!/usr/bin/env python3
"""
Find broken list formatting patterns in markdown files.
"""

import os
import re

def check_file_for_broken_lists(filepath):
    """Check a file for broken list patterns."""
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    issues = []
    for i, line in enumerate(lines):
        # Pattern 1: Line starting with * followed by ** (broken nested list)
        if re.match(r'^\*\s+\*\*', line):
            issues.append((i+1, line.strip(), "Broken nested list with bold"))
        
        # Pattern 2: Line with just **
        if line.strip() == '**':
            issues.append((i+1, line.strip(), "Orphaned bold marker"))
        
        # Pattern 3: Line starting with * after a line with **text (broken list continuation)
        if i > 0 and re.match(r'^\*\s+[^*]', line) and re.match(r'^.*\*\*[^*]+$', lines[i-1]):
            issues.append((i+1, line.strip(), "Broken list continuation"))
    
    return issues

def main():
    """Walk through docs directory and find broken lists."""
    docs_dir = '/home/inocult/projects/studio3-docs/docs'
    total_issues = 0
    
    for root, dirs, files in os.walk(docs_dir):
        for file in files:
            if file.endswith('.md'):
                filepath = os.path.join(root, file)
                issues = check_file_for_broken_lists(filepath)
                if issues:
                    print(f"\n{filepath}:")
                    for line_num, content, issue_type in issues:
                        print(f"  Line {line_num}: {issue_type}")
                        print(f"    Content: {content}")
                    total_issues += len(issues)
    
    print(f"\nTotal issues found: {total_issues}")

if __name__ == "__main__":
    main()