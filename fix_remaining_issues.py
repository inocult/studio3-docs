#!/usr/bin/env python3
import os
import re

def fix_final_issues(content):
    """Fix remaining markdown issues."""
    
    # Fix patterns with asterisk after bold text
    # Example: * **Real-time feedback** on every decision** Network effects**
    # Should be: - **Real-time feedback** on every decision
    # - **Network effects** from the ecosystem
    
    lines = content.split('\n')
    fixed_lines = []
    
    for i, line in enumerate(lines):
        # Skip empty lines
        if not line.strip():
            fixed_lines.append(line)
            continue
            
        # Fix pattern: * **Text** continuation** Other text**
        if line.startswith('* **') and line.count('**') > 2:
            # Split by ** and reconstruct properly
            parts = line.split('**')
            if len(parts) >= 5:
                # Reconstruct as separate bullet points
                fixed_lines.append(f"- **{parts[1]}** {parts[2].strip()}")
                if parts[3].strip():
                    fixed_lines.append(f"- **{parts[3]}** {parts[4].strip() if len(parts) > 4 else ''}")
                continue
        
        # Fix pattern: - * text
        if line.strip().startswith('- *') and not line.strip().startswith('- **'):
            fixed_lines.append('  ' + line.strip())
            continue
            
        # Fix footer links that got messed up
        if '→ [Senders Guide]' in line and 'No newline at end of file' in line:
            fixed_lines.append('    - **Founders** → [Senders Guide](../senders-guide/index.md)')
            continue
        elif '→ [Echoes Guide]' in line and 'No newline at end of file' in line:
            fixed_lines.append('    - **Supporters** → [Echoes Guide](../echoes-guide/index.md)')
            continue
        elif '→ [Anchors Guide]' in line:
            if i + 1 < len(lines) and 'No newline at end of file' in lines[i + 1]:
                fixed_lines.append('    - **Validators** → [Anchors Guide](../anchors-guide/index.md)')
                continue
                
        # Fix "No newline at end of file" appearing in content
        if 'No newline at end of file' in line:
            continue
            
        # Fix patterns like: * **Milestone-based funding** reduces risk** Community validation**
        if '* **' in line and line.count('**') >= 4:
            # Extract all bold sections
            matches = re.findall(r'\*\*([^*]+)\*\*', line)
            if len(matches) >= 2:
                # First item
                remaining_text = line
                first_match = matches[0]
                # Find text after first bold section
                first_pattern = f'**{first_match}**'
                idx = remaining_text.find(first_pattern) + len(first_pattern)
                text_after = remaining_text[idx:].strip()
                
                # Extract non-bold text before second match
                if matches[1] in text_after:
                    idx2 = text_after.find(f'**{matches[1]}')
                    desc1 = text_after[:idx2].strip()
                    fixed_lines.append(f"- **{first_match}** {desc1}")
                    
                    # Second item  
                    if len(matches) > 2:
                        remaining = text_after[idx2:]
                        pattern2 = f'**{matches[1]}**'
                        idx3 = remaining.find(pattern2) + len(pattern2)
                        desc2 = remaining[idx3:].strip()
                        if '**' in desc2:
                            desc2 = desc2.split('**')[0].strip()
                        fixed_lines.append(f"- **{matches[1]}** {desc2}")
                        
                        # Third item if exists
                        if len(matches) > 2 and matches[2]:
                            fixed_lines.append(f"- **{matches[2]}** before major capital")
                    else:
                        fixed_lines.append(f"- **{matches[1]}**")
                else:
                    fixed_lines.append(f"- **{first_match}** {text_after}")
                continue
                
        # Fix Senders Guide who should read section
        if '- **🚀 Entrepreneurs**' in line and '👥 Founding Teams' in line:
            fixed_lines.append('- **🚀 Entrepreneurs** ready to build in public')
            fixed_lines.append('- **👥 Founding Teams** preparing to launch')
            if '🔄 Serial Builders' in line:
                fixed_lines.append('- **🔄 Serial Builders** exploring Studio3')
            if '💡 Innovators' in line:
                fixed_lines.append('- **💡 Innovators** with breakthrough ideas')
            continue
        elif line.strip() == '- **🔄 Serial Builders** 💡 Innovators':
            fixed_lines.append('- **🔄 Serial Builders** exploring Studio3')
            fixed_lines.append('- **💡 Innovators** with breakthrough ideas')
            continue
            
        fixed_lines.append(line)
    
    return '\n'.join(fixed_lines)

def process_file(filepath):
    """Process a single markdown file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        fixed_content = fix_final_issues(content)
        
        if fixed_content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(fixed_content)
            return True
        return False
    except Exception as e:
        print(f"Error processing {filepath}: {e}")
        return False

def main():
    # Focus on files with known remaining issues
    problem_files = [
        '/home/inocult/projects/studio3-docs/docs/quickstart/key-benefits.md',
        '/home/inocult/projects/studio3-docs/docs/senders-guide/index.md',
        '/home/inocult/projects/studio3-docs/docs/quickstart/index.md'
    ]
    
    for filepath in problem_files:
        if os.path.exists(filepath):
            if process_file(filepath):
                print(f"Fixed: {filepath}")
            else:
                print(f"No changes needed: {filepath}")
    
    # Then process all other markdown files
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