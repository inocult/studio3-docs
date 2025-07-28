#!/usr/bin/env python3
"""
Fix specific markdown patterns that are still causing issues
"""

import os
import re
import sys
import glob

def fix_specific_patterns(filepath):
    """Fix specific problematic patterns"""
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        lines = content.split('\n')
    
    fixed_lines = []
    changes_made = 0
    in_code_block = False
    
    for i, line in enumerate(lines):
        original_line = line
        
        # Track code blocks
        if '```' in line:
            in_code_block = not in_code_block
            
        if not in_code_block:
            # Fix pattern: **text** space (something) - space between bold and parens
            line = re.sub(r'(\*\*[^*]+\*\*)\s+(\([^)]+\))', r'\1 \2', line)
            
            # Fix pattern: number. **Text** (percent)** - unclosed bold before parens
            if re.match(r'^\d+\.\s+\*\*[^*]+\*\*\s*\(\d+%\)\*\*', line):
                # This pattern has an extra ** at the end
                line = re.sub(r'^(\d+\.\s+\*\*[^*]+\*\*\s*\(\d+%\))\*\*', r'\1', line)
                
            # Fix patterns like: ** Focus:: **:
            line = re.sub(r'\*\*\s+([\w\s]+)::\s*\*\*:', r'**\1:**', line)
            
            # Fix multiple colons and spaces: :: : becomes :
            line = re.sub(r'::\s*:\s*', ': ', line)
            
            # Fix space before double colon
            line = re.sub(r'\s+::', ':', line)
            
            # Fix URLs with extra colons: https:: : //
            line = re.sub(r'https::\s*:\s*//', 'https://', line)
            line = re.sub(r'http::\s*:\s*//', 'http://', line)
            
            # Fix patterns like: **Pre-Graduation**: text ** Post-Graduation:: **:
            # This is a complex pattern where bold sections are malformed
            if '**' in line and line.count('**') >= 4:
                # Look for pattern: **text**: content ** text:: **:
                match = re.search(r'(\*\*[^*]+\*\*:\s*[^*]+)\s+\*\*\s+([^*]+)::\s*\*\*:', line)
                if match:
                    part1 = match.group(1)
                    part2 = match.group(2)
                    rest = line[match.end():]
                    line = line[:match.start()] + part1 + ' **' + part2 + ':** ' + rest
                    
            # Fix orphaned ** at start of line with capital letter following
            if re.match(r'^\*\*\s+[A-Z]', line):
                line = re.sub(r'^\*\*\s+([A-Z])', r'**\1', line)
                
            # Fix pattern where numbered list has broken bold
            # Like: 1. **Complete self-assessment** using this guide
            # The bold should only wrap the action, not the entire line
            if re.match(r'^\d+\.\s+\*\*[^*]+\s+[^*]+\*\*\s+', line):
                # This indicates split bold text that should be together
                parts = line.split('**')
                if len(parts) >= 3:
                    # Reconstruct properly
                    num_part = parts[0]  # "1. "
                    bold_parts = []
                    rest = ""
                    for j in range(1, len(parts)):
                        if j % 2 == 1:  # Inside bold
                            bold_parts.append(parts[j])
                        else:  # Outside bold
                            if parts[j].strip():
                                rest = parts[j]
                                break
                    if len(bold_parts) == 2 and rest:
                        # Merge the bold parts
                        line = num_part + '**' + bold_parts[0] + ' ' + bold_parts[1] + '** ' + rest
                        
            # Fix h3 tags in arena cards that span multiple lines
            if '<h3>' in line and '</h3>' not in line:
                # Look ahead to see if closing tag is on next line
                if i + 1 < len(lines) and '</h3>' in lines[i + 1]:
                    # Merge lines
                    next_line = lines[i + 1].strip()
                    line = line + ' ' + next_line
                    fixed_lines.append(line)
                    lines[i + 1] = ''  # Clear next line
                    changes_made += 1
                    continue
                    
            # Fix multiple spaces in indented structures (like file trees)
            # Don't fix these - they're intentional for alignment
            if not re.match(r'^\s*[│├└]', line):
                # Fix multiple consecutive spaces not in special structures
                line = re.sub(r'([^\s])\s{2,}([^\s])', r'\1 \2', line)
                
        if line != original_line:
            changes_made += 1
            
        fixed_lines.append(line)
    
    # Remove empty lines created by merging
    final_lines = [line for line in fixed_lines if line is not None]
    
    if changes_made > 0:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write('\n'.join(final_lines))
        print(f"  Fixed {changes_made} patterns in {os.path.basename(filepath)}")
        return changes_made
    return 0

def main():
    """Main entry point"""
    
    # Target specific problem files
    problem_files = [
        'docs/senders-guide/requirements.md',
        'docs/senders-guide/winning-strategies.md',
        'docs/senders-guide/post-graduation.md',
        'docs/senders-guide/mvp-development.md',
        'docs/quickstart/get-started.md',
        'docs/quickstart/what-is-studio3.md',
        'docs/echoes-guide/index.md',
        'docs/overview-guide/interactions.md',
        'docs/anchors-guide/anchor-council.md',
    ]
    
    # Add all other files too
    all_files = glob.glob('docs/**/*.md', recursive=True)
    
    print("🔧 Pattern-Specific Markdown Fixer")
    print(f"Processing {len(all_files)} files...\n")
    
    total_changes = 0
    
    # Process problem files first
    for filepath in problem_files:
        if os.path.exists(filepath):
            changes = fix_specific_patterns(filepath)
            total_changes += changes
    
    # Then process all others
    for filepath in all_files:
        if filepath not in problem_files and os.path.exists(filepath):
            changes = fix_specific_patterns(filepath)
            total_changes += changes
    
    print(f"\n✅ Fixed {total_changes} pattern issues")

if __name__ == "__main__":
    main()