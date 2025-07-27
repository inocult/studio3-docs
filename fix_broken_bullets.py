#!/usr/bin/env python3
import os
import re

def fix_broken_bullet_lists(content):
    """Fix broken bullet list patterns with bold text."""
    
    lines = content.split('\n')
    fixed_lines = []
    i = 0
    
    while i < len(lines):
        line = lines[i]
        
        # Pattern 1: Fix lines like "- **Text**" followed by "- ** continuation"
        if line.strip().startswith('- **') and i + 1 < len(lines):
            next_line = lines[i + 1]
            
            # Check if next line is "- **" with just spaces after
            if re.match(r'^- \*\*\s*[A-Z][a-z]+', next_line.strip()):
                # This is a continuation that should be on the same line
                text_match = re.match(r'^- (\*\*[^*]+)\*\*\s*$', line.strip())
                if text_match:
                    continuation_match = re.match(r'^- \*\*\s*(.+)$', next_line.strip())
                    if continuation_match:
                        fixed_lines.append(f"- {text_match.group(1)}** {continuation_match.group(1)}")
                        i += 2
                        continue
        
        # Pattern 2: Fix pattern "- **Text**\n- ** Continuation**"
        if line.strip().startswith('- **') and line.strip().endswith('**'):
            if i + 1 < len(lines):
                next_line = lines[i + 1]
                if next_line.strip() == '- **' or re.match(r'^- \*\*\s+[A-Z]', next_line.strip()):
                    # Extract the bold text from first line
                    text = line.strip()[2:-2].strip()  # Remove "- " and "**"
                    # Extract continuation from next line
                    if next_line.strip() == '- **' and i + 2 < len(lines):
                        # Look ahead one more line
                        continuation = lines[i + 2].strip()
                        fixed_lines.append(f"- **{text}** {continuation}")
                        i += 3
                        continue
                    else:
                        # Continuation is on the same line
                        cont_match = re.match(r'^- \*\*\s*(.+?)\*\*$', next_line.strip())
                        if cont_match:
                            fixed_lines.append(f"- **{text}** {cont_match.group(1)}")
                            i += 2
                            continue
        
        # Pattern 3: Fix lines that just have "- **" 
        if line.strip() == '- **':
            i += 1
            continue
            
        fixed_lines.append(line)
        i += 1
    
    return '\n'.join(fixed_lines)

def process_file(filepath):
    """Process a single markdown file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        fixed_content = fix_broken_bullet_lists(content)
        
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