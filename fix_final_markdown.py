#!/usr/bin/env python3
import os
import re
import sys

def fix_markdown_comprehensively(content):
    """Fix all markdown rendering issues comprehensively."""
    
    # Fix lines with pattern: **Text:** - Details** or **Text:** Details**
    content = re.sub(r'\*\*([^*:]+)\*\*:\s*-?\s*([^*\n]+)\*\*', r'**\1:** \2', content)
    
    # Fix lines like: - **Text** with continuation on next line starting with - *
    lines = content.split('\n')
    fixed_lines = []
    i = 0
    
    while i < len(lines):
        line = lines[i]
        
        # Check if this line ends with ** and next line starts with - *
        if i + 1 < len(lines) and line.strip().endswith('**'):
            next_line = lines[i + 1]
            if next_line.strip().startswith('- *') or next_line.strip().startswith('* '):
                # Combine the lines properly
                text_match = re.match(r'^(.*\*\*[^*]+)\*\*\s*$', line)
                if text_match:
                    base_text = text_match.group(1)
                    continuation = next_line.strip().lstrip('- *').strip()
                    fixed_lines.append(f"{base_text}** {continuation}")
                    i += 2
                    continue
        
        # Check for pattern: - **Text**\n**- * continuation
        if line.strip().startswith('- **') and i + 1 < len(lines):
            next_line = lines[i + 1]
            if next_line.strip().startswith('**- *'):
                # Extract the bold text and continuation
                text_match = re.match(r'^- (\*\*[^*]+\*\*)\s*$', line.strip())
                if text_match:
                    bold_text = text_match.group(1)
                    continuation = next_line.strip().lstrip('**- *').strip()
                    fixed_lines.append(f"- {bold_text} {continuation}")
                    i += 2
                    continue
        
        # Check for orphaned asterisks on continuation lines
        if line.strip() == '* guiding your journey' or line.strip().startswith('* ') and i > 0:
            prev_line = lines[i - 1] if i > 0 else ''
            if '**' in prev_line and not prev_line.strip().endswith('**'):
                # This is likely a continuation, merge with previous
                if fixed_lines:
                    fixed_lines[-1] = fixed_lines[-1].rstrip() + ' ' + line.strip().lstrip('* ')
                    i += 1
                    continue
        
        # Fix lines that have pattern: * **Text** continuation**
        if line.strip().startswith('* **') and line.strip().endswith('**'):
            # Convert to proper list format
            content_match = re.match(r'^\*\s+(\*\*[^*]+\*\*)\s*(.*)\*\*\s*$', line.strip())
            if content_match:
                bold_part = content_match.group(1)
                rest_part = content_match.group(2).strip()
                if rest_part:
                    fixed_lines.append(f"- {bold_part} {rest_part}")
                else:
                    fixed_lines.append(f"- {bold_part}")
                i += 1
                continue
        
        # Fix lines with trailing ** that shouldn't be there
        if line.endswith('**') and not line.count('**') % 2 == 0:
            line = line.rstrip('*').rstrip()
        
        # Fix double asterisks at line start after whitespace
        line = re.sub(r'^(\s*)\*\*-\s*', r'\1- ', line)
        
        fixed_lines.append(line)
        i += 1
    
    content = '\n'.join(fixed_lines)
    
    # Additional cleanup passes
    # Remove standalone ** lines
    content = re.sub(r'^\s*\*\*\s*$', '', content, flags=re.MULTILINE)
    
    # Fix numbered lists with extra **
    content = re.sub(r'(\d+\.\s+\*\*[^*]+\*\*:[^\n]+)\*\*\s*$', r'\1', content, flags=re.MULTILINE)
    
    # Clean up any quadruple asterisks
    content = re.sub(r'\*{4,}', '**', content)
    
    # Fix patterns where there's a line ending with ** followed by continuation
    content = re.sub(r'\*\*\s*\n\s*\*\*\s*([^\n]+)', r'** \1', content)
    
    return content

def process_file(filepath):
    """Process a single markdown file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        fixed_content = fix_markdown_comprehensively(content)
        
        if fixed_content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(fixed_content)
            return True
        return False
    except Exception as e:
        print(f"Error processing {filepath}: {e}")
        return False

def main():
    # Process specific files with known issues
    problem_files = [
        '/home/inocult/projects/studio3-docs/docs/quickstart/key-benefits.md',
        '/home/inocult/projects/studio3-docs/docs/senders-guide/index.md',
        '/home/inocult/projects/studio3-docs/docs/senders-guide/milestone-planning.md',
        '/home/inocult/projects/studio3-docs/docs/senders-guide/flare-scaling.md',
        '/home/inocult/projects/studio3-docs/docs/senders-guide/building-momentum.md'
    ]
    
    for filepath in problem_files:
        if os.path.exists(filepath):
            if process_file(filepath):
                print(f"Fixed: {filepath}")
            else:
                print(f"No changes needed: {filepath}")
        else:
            print(f"File not found: {filepath}")
    
    # Then process all other markdown files
    docs_dir = '/home/inocult/projects/studio3-docs/docs'
    
    for root, dirs, files in os.walk(docs_dir):
        for file in files:
            if file.endswith('.md'):
                filepath = os.path.join(root, file)
                if filepath not in problem_files:  # Skip already processed
                    if process_file(filepath):
                        print(f"Fixed: {filepath}")

if __name__ == "__main__":
    main()