#!/usr/bin/env python3
"""
Fix the real markdown issues identified by the refined linter
"""

import os
import re
import glob

def fix_specific_issues():
    """Fix the specific issues identified by linter"""
    
    fixes = [
        # Fix missing colons after bold headings
        ('docs/senders-guide/milestone-planning.md', r'1\. \*\*Clear Communication([^:])', r'1. **Clear Communication:**\1'),
        ('docs/senders-guide/founder-basics.md', r'1\. \*\*Clear Communication([^:])', r'1. **Clear Communication:**\1'),
        ('docs/senders-guide/engaging-echoes.md', r'1\. \*\*Clear Guidelines([^:])', r'1. **Clear Guidelines:**\1'),
        
        # Fix broken bullet list formatting patterns
        ('docs/senders-guide/forge-duels.md', r'\*\*\s+- (.+)', r'   - \1'),
        ('docs/senders-guide/duel-preparation.md', r'\*\*\s+- (.+)', r'   - \1'),
        ('docs/senders-guide/mvp-development.md', r'\*\*\s+- (.+)', r'   - \1'),
        ('docs/senders-guide/creating-spark.md', r'\*\*\s+- (.+)', r'   - \1'),
    ]
    
    files_fixed = 0
    
    for file_path, pattern, replacement in fixes:
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                original_content = content
                content = re.sub(pattern, replacement, content, flags=re.MULTILINE)
                
                if content != original_content:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    print(f"Fixed {file_path}")
                    files_fixed += 1
            
            except Exception as e:
                print(f"Error fixing {file_path}: {e}")
    
    return files_fixed

def fix_missing_colons():
    """Fix missing colons after bold headings across all files"""
    docs_dir = 'docs'
    markdown_files = []
    
    for root, dirs, files in os.walk(docs_dir):
        for file in files:
            if file.endswith('.md'):
                markdown_files.append(os.path.join(root, file))
    
    fixes_applied = 0
    
    for file_path in markdown_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            
            # Fix patterns like: **Traditional Way -> **Traditional Way:
            content = re.sub(r'\*\*Traditional Way([^:])', r'**Traditional Way:**\1', content)
            content = re.sub(r'\*\*Studio3 Way([^:])', r'**Studio3 Way:**\1', content)
            content = re.sub(r'\*\*If you have([^:])', r'**If you have:**\1', content)
            content = re.sub(r'\*\*You\'ll need([^:])', r'**You\'ll need:**\1', content)
            content = re.sub(r'\*\*Clear Mechanics([^:])', r'**Clear Mechanics:**\1', content)
            content = re.sub(r'\*\*For All Participants([^:])', r'**For All Participants:**\1', content)
            content = re.sub(r'\*\*Role-Specific([^:])', r'**Role-Specific:**\1', content)
            content = re.sub(r'\*\*Discord Server([^:])', r'**Discord Server:**\1', content)
            content = re.sub(r'\*\*Forum([^:])', r'**Forum:**\1', content)
            content = re.sub(r'\*\*Social Media([^:])', r'**Social Media:**\1', content)
            content = re.sub(r'\*\*How to earn XP([^:])', r'**How to earn XP:**\1', content)
            content = re.sub(r'\*\*Benefits of high XP([^:])', r'**Benefits of high XP:**\1', content)
            content = re.sub(r'\*\*Day 1([^:])', r'**Day 1:**\1', content)
            content = re.sub(r'\*\*Day 2-3([^:])', r'**Day 2-3:**\1', content)
            content = re.sub(r'\*\*Day 4-7([^:])', r'**Day 4-7:**\1', content)
            content = re.sub(r'\*\*For Individuals([^:])', r'**For Individuals:**\1', content)
            content = re.sub(r'\*\*For the Ecosystem([^:])', r'**For the Ecosystem:**\1', content)
            content = re.sub(r'\*\*For the Future([^:])', r'**For the Future:**\1', content)
            content = re.sub(r'\*\*How the community participates([^:])', r'**How the community participates:**\1', content)
            content = re.sub(r'\*\*Example([^:])', r'**Example:**\1', content)
            content = re.sub(r'\*\*If Milestone Succeeds([^:])', r'**If Milestone Succeeds:**\1', content)
            content = re.sub(r'\*\*If Milestone Fails([^:])', r'**If Milestone Fails:**\1', content)
            
            if content != original_content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                fixes_applied += 1
        
        except Exception as e:
            print(f"Error processing {file_path}: {e}")
    
    return fixes_applied

def fix_incomplete_bold():
    """Fix genuinely incomplete bold patterns"""
    docs_dir = 'docs'
    markdown_files = []
    
    for root, dirs, files in os.walk(docs_dir):
        for file in files:
            if file.endswith('.md'):
                markdown_files.append(os.path.join(root, file))
    
    fixes_applied = 0
    
    for file_path in markdown_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            
            # Fix incomplete bold at line endings (but not if it's part of **text**)
            lines = content.split('\n')
            fixed_lines = []
            
            for line in lines:
                # Fix pattern: - **Everyone can succeed 
                if re.search(r'- \*\*[^*]+\s*$', line) and '**' not in line[line.find('**')+2:]:
                    line = line.rstrip() + '**'
                
                # Fix pattern: **Arenas (missing closing)
                if re.search(r'public \*\*Arenas\s*$', line):
                    line = line.replace('**Arenas', '**Arenas**')
                    
                # Fix other incomplete patterns
                if re.search(r'\*\*[^*]+\*(?!\*)', line):
                    line = re.sub(r'\*\*([^*]+)\*(?!\*)', r'**\1**', line)
                
                fixed_lines.append(line)
            
            content = '\n'.join(fixed_lines)
            
            if content != original_content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                fixes_applied += 1
                print(f"Fixed incomplete bold in {file_path}")
        
        except Exception as e:
            print(f"Error processing {file_path}: {e}")
    
    return fixes_applied

def main():
    """Main execution"""
    print("🔧 Fixing real markdown issues...")
    
    specific_fixes = fix_specific_issues()
    colon_fixes = fix_missing_colons()
    bold_fixes = fix_incomplete_bold()
    
    total_fixes = specific_fixes + colon_fixes + bold_fixes
    
    print(f"\n✅ Applied {total_fixes} fixes:")
    print(f"  - Specific issues: {specific_fixes}")
    print(f"  - Missing colons: {colon_fixes}")
    print(f"  - Incomplete bold: {bold_fixes}")
    print("\nRe-run linter to verify fixes")

if __name__ == "__main__":
    main()