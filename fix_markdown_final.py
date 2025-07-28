#!/usr/bin/env python3
"""
Final fix for markdown formatting issues found by linter
"""

import os
import re
import glob

def fix_get_started_file():
    """Fix the specific issues in get-started.md"""
    file_path = 'docs/quickstart/get-started.md'
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Fix broken numbered lists with double asterisks
    fixes = [
        # Fix: **2. **Create your account** and connect wallet
        (r'(\d+)\.\s+\*\*([^*]+)\*\*\s+and\s+([^*\n]+)', r'\1. **\2** and \3'),
        (r'(\d+)\.\s+\*\*([^*]+)\*\*\s+to\s+([^*\n]+)', r'\1. **\2** to \3'),
        (r'(\d+)\.\s+\*\*([^*]+)\*\*\s+with\s+([^*\n]+)', r'\1. **\2** with \3'),
        (r'(\d+)\.\s+\*\*([^*]+)\*\*\s+for\s+([^*\n]+)', r'\1. **\2** for \3'),
        (r'(\d+)\.\s+\*\*([^*]+)\*\*\s+on\s+([^*\n]+)', r'\1. **\2** on \3'),
        (r'(\d+)\.\s+\*\*([^*]+)\*\*\s+-\s+([^*\n]+)', r'\1. **\2** - \3'),
        
        # Fix broken patterns like **2. **Signal Mechanics** - Description
        (r'\*\*(\d+)\.\s+\*\*([^*]+)\*\*\s+-\s+([^*\n]+)', r'\1. **\2** - \3'),
        (r'\*\*(\d+)\.\s+\*\*([^*]+)\*\*\s+([^*\n]+)', r'\1. **\2** \3'),
        
        # Fix lines that end with incomplete formatting
        (r'([^*])\*\*\s*$', r'\1'),
        
        # Fix broken patterns in lists
        (r'^\*\*([^*]+):\*\*', r'**\1:**'),
        (r'^\*\*([^*]+)\*\*:', r'**\1:**'),
        
        # Fix broken arena card content
        (r'- \*\*([^*]+)\s+-\s+([^*\n]+)', r'- **\1** - \2'),
    ]
    
    original_content = content
    for pattern, replacement in fixes:
        content = re.sub(pattern, replacement, content, flags=re.MULTILINE)
    
    # Additional specific fixes for get-started.md
    specific_fixes = [
        # Fix the numbered list at the beginning
        ('1. **Choose your role** based on your goals\n**2. **Create your account** and connect wallet\n**3. **Start small** to learn the system\n**4. **Engage actively** with the community\n**5. **Build your reputation** over time',
         '1. **Choose your role** based on your goals\n2. **Create your account** and connect wallet\n3. **Start small** to learn the system\n4. **Engage actively** with the community\n5. **Build your reputation** over time'),
         
        # Fix the account setup process
        ('1. **Install MetaMask** or compatible wallet\n**2. **Fund with ETH** for gas fees\n**3. **Acquire $SIGNAL** tokens via DEX\n**4. **Connect to Studio3** platform\n**5. **Complete profile** with real information\n**6. **Verify email** for notifications\n**7. **Join Discord** community',
         '1. **Install MetaMask** or compatible wallet\n2. **Fund with ETH** for gas fees\n3. **Acquire $SIGNAL** tokens via DEX\n4. **Connect to Studio3** platform\n5. **Complete profile** with real information\n6. **Verify email** for notifications\n7. **Join Discord** community'),
         
        # Fix the key concepts section
        ('1. **The Arena System** - How public building works\n**2. **Signal Mechanics** - Belief/doubt token stakes\n**3. **Seven Phases** - Venture progression path\n**4. **Rewards & Burns** - Economic incentives\n**5. **Reputation (XP)** - Long-term value building',
         '1. **The Arena System** - How public building works\n2. **Signal Mechanics** - Belief/doubt token stakes\n3. **Seven Phases** - Venture progression path\n4. **Rewards & Burns** - Economic incentives\n5. **Reputation (XP)** - Long-term value building'),
         
        # Fix building relationships section
        ('1. **Introduce yourself** in newcomer channels\n**2. **Ask questions** - community loves helping\n**3. **Share insights** from your experience\n**4. **Attend events** like office hours\n**5. **Find mentors** who\'ve succeeded',
         '1. **Introduce yourself** in newcomer channels\n2. **Ask questions** - community loves helping\n3. **Share insights** from your experience\n4. **Attend events** like office hours\n5. **Find mentors** who\'ve succeeded'),
         
        # Fix long-term strategy
        ('1. **Consistency beats intensity** - Daily engagement\n**2. **Quality over quantity** - Thoughtful participation\n**3. **Learn from failures** - They\'re valuable too\n**4. **Share knowledge** - Teaching solidifies learning\n**5. **Stay positive** - Support ecosystem growth',
         '1. **Consistency beats intensity** - Daily engagement\n2. **Quality over quantity** - Thoughtful participation\n3. **Learn from failures** - They\'re valuable too\n4. **Share knowledge** - Teaching solidifies learning\n5. **Stay positive** - Support ecosystem growth'),
         
        # Fix what happens next section
        ('1. **Week 1**: Learn and observe\n**2. **Week 2-4**: Active participation\n**3. **Month 2-3**: Build reputation\n**4. **Month 4-6**: Scale involvement\n**5. **Month 6+**: Become veteran helper',
         '1. **Week 1**: Learn and observe\n2. **Week 2-4**: Active participation\n3. **Month 2-3**: Build reputation\n4. **Month 4-6**: Scale involvement\n5. **Month 6+**: Become veteran helper'),
         
        # Fix continue your journey section
        ('1. **Dive deeper** with the [Overview Guide](../overview-guide/index.md)\n**2. **Master your role** with specific guides\n**3. **Join the community** on [Discord](https://discord.gg/studio3)\n**4. **Start participating** today',
         '1. **Dive deeper** with the [Overview Guide](../overview-guide/index.md)\n2. **Master your role** with specific guides\n3. **Join the community** on [Discord](https://discord.gg/studio3)\n4. **Start participating** today'),
         
        # Fix broken patterns with double asterisks at the end
        ('- **Great ideas find support** - Merit beats connections** ',
         '- **Great ideas find support** - Merit beats connections'),
         
        ('- **Transparency builds trust** - Community creates value** ',
         '- **Transparency builds trust** - Community creates value'),
         
        ('- **Everyone can succeed** ',
         '- **Everyone can succeed**'),
    ]
    
    for old, new in specific_fixes:
        content = content.replace(old, new)
    
    if content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Fixed get-started.md")
        return True
    return False

def fix_markdown_files():
    """Fix markdown files with common patterns"""
    docs_dir = 'docs'
    markdown_files = []
    
    for root, dirs, files in os.walk(docs_dir):
        for file in files:
            if file.endswith('.md'):
                markdown_files.append(os.path.join(root, file))
    
    total_fixed = 0
    
    for file_path in markdown_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            
            # Fix broken numbered lists
            content = re.sub(r'\*\*(\d+)\.\s+\*\*([^*\n]+)\*\*', r'\1. **\2**', content)
            content = re.sub(r'\*\*(\d+)\.\s+\*\*([^*\n]+)', r'\1. **\2**', content)
            
            # Fix trailing double asterisks
            content = re.sub(r'([^*])\*\*\s*$', r'\1', content, flags=re.MULTILINE)
            content = re.sub(r'([^*])\*\*\s*\n', r'\1\n', content, flags=re.MULTILINE)
            
            # Fix broken bold patterns in lists
            content = re.sub(r'^(\d+)\.\s+\*\*([^*\n]+)\*\*\*\*', r'\1. **\2**', content, flags=re.MULTILINE)
            
            if content != original_content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                total_fixed += 1
                print(f"Fixed {file_path}")
        
        except Exception as e:
            print(f"Error processing {file_path}: {e}")
    
    return total_fixed

def main():
    """Main execution"""
    print("🔧 Fixing markdown formatting issues...")
    
    # Fix get-started.md specifically
    get_started_fixed = fix_get_started_file()
    
    # Fix all other files
    files_fixed = fix_markdown_files()
    
    print(f"\n✅ Fixed {files_fixed + (1 if get_started_fixed else 0)} files")
    print("Re-run linter to check remaining issues")

if __name__ == "__main__":
    main()