#!/usr/bin/env python3
import os
import re

def fix_markdown_issues(content):
    """Fix all markdown rendering issues."""
    
    # Fix pattern: - **Text** continuation
    # Should be: - **Text** continuation
    lines = content.split('\n')
    fixed_lines = []
    
    for i, line in enumerate(lines):
        # Skip empty lines
        if not line.strip():
            fixed_lines.append(line)
            continue
            
        # Fix specific patterns
        fixed_line = line
        
        # Pattern: "- **Great ideas** Community wisdom**"
        # Should be: "- **Great ideas** don't die from lack of resources"
        if '- **Great ideas**' in line and 'Community wisdom**' in line:
            fixed_line = "- **Great ideas** don't die from lack of resources"
        elif line.strip() == '- **Community wisdom**':
            fixed_line = "- **Community wisdom** guides venture development"
        elif '- **Transparent progress**' in line and 'Everyone wins**' in line:
            fixed_line = "- **Transparent progress** replaces closed-door decisions"
        elif line.strip() == '- **Everyone wins**':
            fixed_line = "- **Everyone wins** when ventures succeed"
            
        # Pattern: "- **Saves time** Clarifies concepts**"
        elif '- **Saves time**' in line and 'Clarifies concepts**' in line:
            fixed_line = "- **Saves time** - Get the essence without the details"
        elif line.strip() == '- **Clarifies concepts**':
            fixed_line = "- **Clarifies concepts** - Simple language, no jargon"
        elif '- **Helps you decide**' in line and 'Points the way**' in line:
            fixed_line = "- **Helps you decide** - Is Studio3 right for you?"
        elif line.strip() == '- **Points the way**':
            fixed_line = "- **Points the way** - Know where to go next"
            
        # Fix SMART-V pattern
        elif line.strip() == '- ****M** A':
            fixed_line = "- **M**easurable - Quantifiable outcomes"
        elif line.strip() == '- ****R** T':
            fixed_line = "- **A**chievable - Realistic yet ambitious"
            fixed_lines.append(fixed_line)
            fixed_line = "- **R**elevant - Aligned with phase goals"
            fixed_lines.append(fixed_line)
            fixed_line = "- **T**ime-bound - Clear deadline"
            
        # Fix Dependency Types
        elif '**Dependency Types:** Sequential**' in line:
            fixed_line = '**Dependency Types:**'
            fixed_lines.append(fixed_line)
            fixed_line = '- **Sequential** - Must complete A before B'
        elif '- **Parallel** Conditional**' in line:
            fixed_line = '- **Parallel** - Can do simultaneously'
            fixed_lines.append(fixed_line)
            fixed_line = '- **Conditional** - If A then B'
        elif '- **External** Resource**' in line:
            fixed_line = '- **External** - Outside dependencies'
            fixed_lines.append(fixed_line)
            fixed_line = '- **Resource** - Shared constraints'
            
        # Fix 70-20-10 Rule
        elif '**The 70-20-10 Rule:** 70% Confidence**' in line:
            fixed_line = '**The 70-20-10 Rule:**'
            fixed_lines.append(fixed_line)
            fixed_line = '- **70% Confidence** - Core milestones'
        elif line.strip() == '- **20% Stretch**':
            fixed_line = '- **20% Stretch** - Ambitious targets'
        elif '- ** 10% Moonshot** Risk-Reward Matrix:**' in line:
            fixed_line = '- **10% Moonshot** - Breakthrough goals'
            
        # Fix other common patterns
        elif '**Traditional Way:**' in line and ' - ' in line:
            parts = line.split('**Traditional Way:**')
            fixed_line = parts[0] + '**Traditional Way:**'
            fixed_lines.append(fixed_line)
            rest = parts[1].strip()
            fixed_line = rest if rest.startswith('- ') else '- ' + rest.lstrip('- ')
        elif '**Studio3 Way:**' in line and ' - ' in line:
            parts = line.split('**Studio3 Way:**')
            fixed_line = parts[0] + '**Studio3 Way:**'
            fixed_lines.append(fixed_line)
            rest = parts[1].strip()
            fixed_line = rest if rest.startswith('- ') else '- ' + rest.lstrip('- ')
            
        # Remove trailing ** that shouldn't be there
        if fixed_line.count('**') % 2 != 0 and fixed_line.endswith('**'):
            fixed_line = fixed_line[:-2].rstrip()
            
        fixed_lines.append(fixed_line)
    
    return '\n'.join(fixed_lines)

def process_file(filepath):
    """Process a single markdown file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        fixed_content = fix_markdown_issues(content)
        
        if fixed_content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(fixed_content)
            return True
        return False
    except Exception as e:
        print(f"Error processing {filepath}: {e}")
        return False

def main():
    # Process specific problem files
    problem_files = [
        '/home/inocult/projects/studio3-docs/docs/quickstart/index.md',
        '/home/inocult/projects/studio3-docs/docs/quickstart/key-benefits.md',
        '/home/inocult/projects/studio3-docs/docs/senders-guide/milestone-planning.md',
        '/home/inocult/projects/studio3-docs/docs/senders-guide/index.md',
        '/home/inocult/projects/studio3-docs/docs/senders-guide/building-momentum.md'
    ]
    
    for filepath in problem_files:
        if os.path.exists(filepath):
            if process_file(filepath):
                print(f"Fixed: {filepath}")
            else:
                print(f"No changes needed: {filepath}")

if __name__ == "__main__":
    main()