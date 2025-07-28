#!/usr/bin/env python3
"""
Fix specific formatting issues in get-started.md file.
"""

import re

def fix_get_started_content(content):
    """Fix all the broken formatting in get-started.md"""
    
    # Split into lines for easier processing
    lines = content.split('\n')
    fixed_lines = []
    changes_made = 0
    
    for i, line in enumerate(lines):
        original_line = line
        
        # Fix running numbered lists without proper line breaks
        # Pattern: 1. **text**2. **text**3. **text**
        if re.search(r'\d+\.\s*\*\*[^*]+\*\*\d+\.\s*\*\*', line):
            # Split on numbered items
            parts = re.split(r'(\d+\.\s*\*\*[^*]+\*\*)', line)
            new_lines = []
            for part in parts:
                if part.strip() and re.match(r'\d+\.\s*\*\*[^*]+\*\*', part):
                    new_lines.append(part)
                elif part.strip():
                    new_lines.append(part)
            
            if len(new_lines) > 1:
                # Add first line, then others as separate lines
                line = new_lines[0]
                for j in range(1, len(new_lines)):
                    fixed_lines.append(line)
                    line = new_lines[j]
                changes_made += 1
        
        # Fix broken numbered list patterns: **text**## Header
        if re.search(r'\*\*[^*]*\*\*##\s*', line):
            line = re.sub(r'(\*\*[^*]*\*\*)##\s*([A-Z])', r'\1\n\n## \2', line)
            changes_made += 1
        
        # Fix patterns like: -**text**
        line = re.sub(r'^-\s*\*\*([^*]+)\*\*\s*$', r'- **\1**', line)
        if line != original_line:
            changes_made += 1
            original_line = line
        
        # Fix patterns like: - **text** more content
        line = re.sub(r'^-\s*\*\*([^*]+)\*\*(.+)$', r'- **\1**\2', line)
        if line != original_line:
            changes_made += 1
            original_line = line
        
        # Fix broken numbered lists that run together
        # Pattern: text**## Header
        line = re.sub(r'([a-zA-Z])\*\*##\s*([A-Z])', r'\1\n\n## \2', line)
        if line != original_line:
            changes_made += 1
            original_line = line
        
        # Fix patterns like: 5. **text****## Header
        line = re.sub(r'(\d+\.\s*\*\*[^*]+\*\*)\*\*##\s*([A-Z])', r'\1\n\n## \2', line)
        if line != original_line:
            changes_made += 1
            original_line = line
        
        # Fix standalone ** at end of lines
        line = re.sub(r'\*\*\s*$', '', line)
        if line != original_line:
            changes_made += 1
            original_line = line
        
        # Fix missing line breaks before headers
        if line.startswith('## ') and i > 0 and fixed_lines and fixed_lines[-1].strip() and not fixed_lines[-1].startswith('#'):
            fixed_lines.append('')
            changes_made += 1
        
        # Fix patterns like: -****text**: content**
        line = re.sub(r'-\s*\*\*\*\*([^*:]+):\*\*([^*]*)\*\*', r'- **\1:** \2', line)
        if line != original_line:
            changes_made += 1
            original_line = line
        
        # Fix patterns where content runs together with no line breaks
        # Example: content**text**: more content
        line = re.sub(r'([a-zA-Z])\*\*([A-Z][^*:]+):\*\*', r'\1\n\n**\2:**', line)
        if line != original_line:
            changes_made += 1
            original_line = line
        
        fixed_lines.append(line)
    
    # Now do a second pass to fix specific patterns that might span multiple lines
    content = '\n'.join(fixed_lines)
    
    # Fix specific broken patterns found in the file
    fixes = [
        # Fix the opening list
        (r'1\. \*\*Choose your role\*\* based on your goals\*\*2\. \*\*Create your account\*\* and connect wallet\*\*3\. \*\*Start small\*\* to learn the system\*\*4\. \*\*Engage actively\*\* with the community\*\*5\. \*\*Build your reputation\*\* over time\*\*',
         '1. **Choose your role** based on your goals\n2. **Create your account** and connect wallet\n3. **Start small** to learn the system\n4. **Engage actively** with the community\n5. **Build your reputation** over time'),
        
        # Fix account setup list
        (r'1\.\*\*Install MetaMask\*\* or compatible wallet\*\*2\. \*\*Fund with ETH\*\* for gas fees\*\*3\. \*\*Acquire \$SIGNAL\*\* tokens via DEX\*\*4\. \*\*Connect to Studio3\*\* platform\*\*5\. \*\*Complete profile\*\* with real information\*\*6\. \*\*Verify email\*\* for notifications\*\*7\. \*\*Join Discord\*\* community\*\*',
         '1. **Install MetaMask** or compatible wallet\n2. **Fund with ETH** for gas fees\n3. **Acquire $SIGNAL** tokens via DEX\n4. **Connect to Studio3** platform\n5. **Complete profile** with real information\n6. **Verify email** for notifications\n7. **Join Discord** community'),
        
        # Fix other running numbered lists
        (r'(\d+)\.\s*\*\*([^*]+)\*\*([^*]*)\*\*(\d+)\.\s*\*\*', r'\1. **\2**\3\n\4. **'),
        
        # Fix broken patterns with headers
        (r'\*\*## ', r'\n\n## '),
        
        # Fix specific patterns in the file
        (r'1\.\*\*Web3 Wallet\*\*', r'1. **Web3 Wallet**'),
        (r'2\.\*\*\$SIGNAL Tokens\*\*', r'2. **$SIGNAL Tokens**'),
        (r'3\.\*\*Platform Access\*\*', r'3. **Platform Access**'),
        
        # Fix the knowledge section
        (r'- 1\.\*\*The Arena System\*\*', r'1. **The Arena System**'),
        (r'2\. \*\*Signal Mechanics\*\*', r'2. **Signal Mechanics**'),
        (r'3\. \*\*Seven Phases\*\*', r'3. **Seven Phases**'),
        (r'4\. \*\*Rewards & Burns\*\*', r'4. **Rewards & Burns**'),
        (r'5\. \*\*Reputation \(XP\)\*\*', r'5. **Reputation (XP)**'),
        
        # Fix engagement section
        (r'1\.\*\*Introduce yourself\*\*', r'1. **Introduce yourself**'),
        (r'2\. \*\*Ask questions\*\*', r'2. **Ask questions**'),
        (r'3\. \*\*Share insights\*\*', r'3. **Share insights**'),
        (r'4\. \*\*Attend events\*\*', r'4. **Attend events**'),
        (r'5\. \*\*Find mentors\*\*', r'5. **Find mentors**'),
        
        # Fix reputation section
        (r'- 1\.\*\*Consistency beats intensity\*\*', r'1. **Consistency beats intensity**'),
        (r'2\. \*\*Quality over quantity\*\*', r'2. **Quality over quantity**'),
        (r'3\. \*\*Learn from failures\*\*', r'3. **Learn from failures**'),
        (r'4\. \*\*Share knowledge\*\*', r'4. **Share knowledge**'),
        (r'5\. \*\*Stay positive\*\*', r'5. **Stay positive**'),
        
        # Fix journey section
        (r'1\.\*\*Week 1\*\*', r'1. **Week 1**'),
        (r'2\. \*\*Week 2-4\*\*', r'2. **Week 2-4**'),
        (r'3\. \*\*Month 2-3\*\*', r'3. **Month 2-3**'),
        (r'4\. \*\*Month 4-6\*\*', r'4. **Month 4-6**'),
        (r'5\. \*\*Month 6\+\*\*', r'5. **Month 6+**'),
        
        # Fix success metrics
        (r'- \*\*Community recognizes\*\*', r'- **Community recognizes**'),
        (r'-\*\*\*\*Actions succeed\*\*', r'- **Actions succeed**'),
        (r'-\*\*Reputation grows\*\*', r'- **Reputation grows**'),
        (r'-\*\*Opportunities increase\*\*', r'- **Opportunities increase**'),
        (r'-\*\*You help newcomers\*\*', r'- **You help newcomers**'),
        
        # Fix final sections
        (r'-\*\*Great ideas find support\*\*', r'- **Great ideas find support**'),
        (r'-\*\*\*\*Transparency builds trust\*\*', r'- **Transparency builds trust**'),
        (r'-\*\*\*\*Everyone can succeed\*\*\*\*', r'- **Everyone can succeed**'),
        
        # Fix quick links
        (r'1\.\*\*Dive deeper\*\*', r'1. **Dive deeper**'),
        (r'2\. \*\*Master your role\*\*', r'2. **Master your role**'),
        (r'3\. \*\*Join the community\*\*', r'3. **Join the community**'),
        (r'4\. \*\*Start participating\*\*', r'4. **Start participating**'),
        
        # Fix links section
        (r'- \*\*Platform\*\*:', r'- **Platform**:'),
        (r'-\*\*\*\*Support\*\*:', r'- **Support**:'),
        (r'-\*\*\*\*Discord\*\*:', r'- **Discord**:'),
        (r'-\*\*\*\*Twitter\*\*:', r'- **Twitter**:'),
        
        # Clean up excessive asterisks
        (r'\*{4,}', r'**'),
        
        # Fix final admonition
        (r'\*\*\!\!\! success', r'\n\n!!! success'),
        (r'\*\*Remember\*\*:', r'**Remember**:'),
    ]
    
    for pattern, replacement in fixes:
        old_content = content
        content = re.sub(pattern, replacement, content)
        if content != old_content:
            changes_made += 1
    
    return content, changes_made

def main():
    """Fix the get-started.md file specifically."""
    file_path = "docs/quickstart/get-started.md"
    
    print("🔧 Fixing get-started.md formatting...")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        fixed_content, changes = fix_get_started_content(content)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(fixed_content)
        
        print(f"✅ Fixed {changes} formatting issues in get-started.md")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()