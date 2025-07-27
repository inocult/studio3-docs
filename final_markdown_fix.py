#!/usr/bin/env python3
import os
import re

def fix_specific_patterns(content):
    """Fix specific markdown patterns that are causing rendering issues."""
    
    # Fix pattern where there's text after bold with asterisk
    # Example: **Expert mentors** * guiding your journey
    # Should be: **Expert mentors** guiding your journey
    content = re.sub(r'(\*\*[^*]+\*\*)\s*\*\s+([^*\n]+)', r'\1 \2', content)
    
    # Fix pattern where line has text at the end of a file
    content = re.sub(r'\n\s*No newline at end of file\s*\n', '\n', content)
    
    # Fix the pattern where we have incomplete list items
    # Pattern: - **Text**\n- ** Next item**
    # Should be: - **Text**\n- **Next item**
    content = re.sub(r'^(\s*-\s*)\*\*\s+([^*]+\*\*)$', r'\1**\2', content, flags=re.MULTILINE)
    
    # Fix SMART-V criteria that got broken
    lines = content.split('\n')
    fixed_lines = []
    i = 0
    
    while i < len(lines):
        line = lines[i]
        
        # Fix SMART-V pattern
        if '**SMART-V Criteria:**' in line:
            fixed_lines.append('**SMART-V Criteria:**')
            # Check if next lines are the criteria
            if i + 1 < len(lines) and '**S**pecific' in lines[i + 1]:
                fixed_lines.append('- **S**pecific - Clear and unambiguous')
                i += 1
                # Look for the rest of the criteria on following lines
                j = i + 1
                while j < len(lines) and j < i + 10:
                    if '**M**' in lines[j]:
                        fixed_lines.append('- **M**easurable - Quantifiable outcomes')
                    elif '**A**' in lines[j]:
                        fixed_lines.append('- **A**chievable - Realistic yet ambitious')
                    elif '**R**' in lines[j]:
                        fixed_lines.append('- **R**elevant - Aligned with phase goals')
                    elif '**T**' in lines[j]:
                        fixed_lines.append('- **T**ime-bound - Clear deadline')
                    elif '**V**erifiable' in lines[j]:
                        fixed_lines.append('- **V**erifiable - Provable to Anchors')
                        i = j
                        break
                    elif lines[j].strip() and not lines[j].strip().startswith('-'):
                        # Hit something else, stop looking
                        i = j - 1
                        break
                    j += 1
                i += 1
                continue
        
        # Fix pattern where we have orphaned list continuations
        if line.strip() == '- **' or line.strip() == '**':
            i += 1
            continue
        
        # Fix Studio3 Advantages pattern
        if '**Studio3 Advantages:**' in line and ' - ' in line:
            parts = line.split('**Studio3 Advantages:**')
            fixed_lines.append(parts[0] + '**Studio3 Advantages:**')
            rest = parts[1].strip()
            if rest.startswith('- '):
                fixed_lines.append(rest)
            else:
                fixed_lines.append('- ' + rest.lstrip('- '))
            i += 1
            continue
        
        # Fix patterns like: **For Individuals:** - text
        patterns = [
            '**For Individuals:**',
            '**For the Ecosystem:**', 
            '**For the Future:**',
            '**Traditional Startup Failure Rate:**'
        ]
        
        for pattern in patterns:
            if pattern in line and ' - ' in line:
                parts = line.split(pattern)
                if len(parts) == 2:
                    fixed_lines.append(parts[0] + pattern)
                    rest = parts[1].strip()
                    if rest.startswith('- '):
                        fixed_lines.append(rest)
                    else:
                        fixed_lines.append('- ' + rest.lstrip('- '))
                    i += 1
                    break
        else:
            # Pattern not found, add line as is
            fixed_lines.append(line)
            i += 1
    
    content = '\n'.join(fixed_lines)
    
    # Fix the end of file links
    # Pattern: **    - **Supporters** → ...
    content = re.sub(r'\*\*\s*-\s*\*\*([^*]+)\*\*', r'    - **\1**', content)
    
    # Fix bullet points that got merged
    # Pattern: - **Text1** Text2**
    content = re.sub(r'^(\s*-\s*\*\*[^*]+\*\*)\s+([^*\s][^*]*)\*\*$', r'\1 \2', content, flags=re.MULTILINE)
    
    # Clean up any remaining double/triple asterisks
    content = re.sub(r'\*{3,}', '**', content)
    
    # Fix incomplete list items at the end of sections
    content = re.sub(r'^(\s*-\s*\*\*[^*]+)\s*$', r'\1**', content, flags=re.MULTILINE)
    
    return content

def process_file(filepath):
    """Process a single markdown file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        fixed_content = fix_specific_patterns(content)
        
        if fixed_content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(fixed_content)
            return True
        return False
    except Exception as e:
        print(f"Error processing {filepath}: {e}")
        return False

def main():
    # Focus on files with known issues
    problem_files = [
        '/home/inocult/projects/studio3-docs/docs/quickstart/key-benefits.md',
        '/home/inocult/projects/studio3-docs/docs/senders-guide/index.md',
        '/home/inocult/projects/studio3-docs/docs/senders-guide/milestone-planning.md',
        '/home/inocult/projects/studio3-docs/docs/senders-guide/building-momentum.md'
    ]
    
    for filepath in problem_files:
        if os.path.exists(filepath):
            if process_file(filepath):
                print(f"Fixed: {filepath}")
            else:
                print(f"No changes needed: {filepath}")
    
    # Then process all markdown files
    docs_dir = '/home/inocult/projects/studio3-docs/docs'
    
    for root, dirs, files in os.walk(docs_dir):
        for file in files:
            if file.endswith('.md'):
                filepath = os.path.join(root, file)
                if filepath not in problem_files:
                    if process_file(filepath):
                        print(f"Fixed: {filepath}")

if __name__ == "__main__":
    main()