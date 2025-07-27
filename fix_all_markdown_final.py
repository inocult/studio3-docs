#!/usr/bin/env python3
import os
import re

def fix_markdown_completely(content):
    """Fix all markdown rendering issues completely."""
    
    lines = content.split('\n')
    fixed_lines = []
    i = 0
    
    while i < len(lines):
        line = lines[i]
        
        # Skip empty lines
        if not line.strip():
            fixed_lines.append(line)
            i += 1
            continue
        
        # Fix pattern: **Traditional Way:** - text
        # Should be: **Traditional Way:**\n- text
        if '**Traditional Way:**' in line and ' - ' in line:
            parts = line.split('**Traditional Way:**')
            if len(parts) == 2:
                fixed_lines.append(parts[0] + '**Traditional Way:**')
                rest = parts[1].strip()
                if rest.startswith('- '):
                    fixed_lines.append(rest)
                else:
                    fixed_lines.append('- ' + rest.lstrip('- '))
                i += 1
                continue
        
        # Fix pattern: **Studio3 Way:** - text
        if '**Studio3 Way:**' in line and ' - ' in line:
            parts = line.split('**Studio3 Way:**')
            if len(parts) == 2:
                fixed_lines.append(parts[0] + '**Studio3 Way:**')
                rest = parts[1].strip()
                if rest.startswith('- '):
                    fixed_lines.append(rest)
                else:
                    fixed_lines.append('- ' + rest.lstrip('- '))
                i += 1
                continue
        
        # Fix lines ending with ** and next line having continuation
        if line.strip().endswith('**') and i + 1 < len(lines):
            next_line = lines[i + 1]
            
            # Pattern: - **Text** followed by continuation
            if line.strip().startswith('- **') and (next_line.strip().startswith('- *') or next_line.strip().startswith('* ')):
                # Extract the bold text
                match = re.match(r'^(.*- \*\*[^*]+)\*\*\s*$', line)
                if match:
                    base = match.group(1)
                    continuation = next_line.strip().lstrip('- *').strip()
                    fixed_lines.append(f"{base}** {continuation}")
                    i += 2
                    continue
        
        # Fix lines with orphaned asterisks
        if line.strip().startswith('* ') and not line.strip().startswith('* **'):
            # Check if previous line has incomplete bold
            if i > 0 and fixed_lines and '**' in fixed_lines[-1]:
                # This is a continuation line
                continuation = line.strip().lstrip('* ').strip()
                fixed_lines[-1] = fixed_lines[-1].rstrip() + ' ' + continuation
                i += 1
                continue
        
        # Fix pattern: **Text:** stuff**
        # Should be: **Text:** stuff
        line = re.sub(r'(\*\*[^*:]+\*\*:)([^*\n]+)\*\*', r'\1\2', line)
        
        # Fix numbered lists pattern
        line = re.sub(r'^(\d+\.\s+\*\*[^*]+\*\*:?[^*\n]*)\*\*\s*$', r'\1', line)
        
        # Fix pattern where line ends with multiple **
        if line.count('**') > 0 and line.rstrip().endswith('**'):
            # Count the asterisks
            stripped = line.rstrip()
            if stripped.count('**') % 2 != 0:
                line = stripped.rstrip('*').rstrip()
        
        # Fix **Clear Mechanics:** pattern
        if '**Clear Mechanics:**' in line:
            parts = line.split('**Clear Mechanics:**')
            if len(parts) == 2 and parts[1].strip().startswith('-'):
                fixed_lines.append(parts[0] + '**Clear Mechanics:**')
                fixed_lines.append(parts[1].strip())
                i += 1
                continue
        
        # Fix any quadruple asterisks
        line = line.replace('****', '**')
        
        # Fix - **Text** pattern at the beginning
        line = re.sub(r'^(\s*)\*\*-\s*\*\*', r'\1- **', line)
        
        # Fix bullet points that merged incorrectly
        # Pattern: - **Text1** Text2** Text3**
        # Should be separate lines
        if line.startswith('- **') and line.count('**') > 2:
            # Special handling for these lines
            parts = re.findall(r'\*\*[^*]+\*\*', line)
            if len(parts) > 1:
                # First part stays on this line
                fixed_lines.append(f"- {parts[0]}")
                # Rest become new bullet points
                for part in parts[1:]:
                    fixed_lines.append(f"- {part}")
                i += 1
                continue
        
        fixed_lines.append(line)
        i += 1
    
    content = '\n'.join(fixed_lines)
    
    # Final cleanup passes
    # Remove standalone ** lines
    content = re.sub(r'^\s*\*\*\s*$', '', content, flags=re.MULTILINE)
    
    # Fix SMART-V pattern specifically
    content = re.sub(r'\*\*SMART-V Criteria:\*\*\s*([A-Z]\*\*[^*]+\*\*)', r'**SMART-V Criteria:**\n- **\1', content)
    
    # Fix patterns where bold text is split across lines incorrectly
    content = re.sub(r'\*\*\s*\n\s*\*\*', '**\n', content)
    
    return content

def process_file(filepath):
    """Process a single markdown file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        fixed_content = fix_markdown_completely(content)
        
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