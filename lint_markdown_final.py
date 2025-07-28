#!/usr/bin/env python3
"""
Final comprehensive markdown linter with arena-card rendering rules
Detects and optionally fixes all markdown rendering issues
"""

import os
import re
import sys
import glob
import yaml
from pathlib import Path

class FinalMarkdownLinter:
    def __init__(self):
        self.errors = []
        self.warnings = []
        self.file_count = 0
        self.fixes_applied = 0
        
    def add_error(self, file_path, line_num, message):
        self.errors.append(f"{file_path}:{line_num}: ERROR: {message}")
        
    def add_warning(self, file_path, line_num, message):
        self.warnings.append(f"{file_path}:{line_num}: WARNING: {message}")
    
    def check_arena_card_lists(self, content, file_path):
        """Check for improperly formatted lists in arena cards"""
        lines = content.split('\n')
        in_arena_card = False
        arena_depth = 0
        
        for i, line in enumerate(lines, 1):
            if '<div class="arena-card"' in line:
                in_arena_card = True
                arena_depth += 1
                # Check for markdown="1" attribute
                if 'markdown="1"' not in line and line.strip().endswith('>'):
                    self.add_warning(file_path, i, "Arena card missing markdown=\"1\" attribute")
            
            elif '</div>' in line and in_arena_card:
                arena_depth -= 1
                if arena_depth == 0:
                    in_arena_card = False
            
            elif in_arena_card and line.strip():
                # Check for multiple list items on same line
                # Pattern: "- item1 - item2 - item3"
                if line.startswith('-') and line.count(' - ') >= 1:
                    self.add_error(file_path, i, f"Multiple bullet items on same line: {line.strip()[:60]}...")
                
                # Pattern: "**Header:** - item1 - item2"
                if re.match(r'^\*\*[^*]+:\*\*\s*-\s*', line) and ' - ' in line:
                    self.add_error(file_path, i, f"List items inline with header: {line.strip()[:60]}...")
                
                # Pattern: numbered lists on same line
                if re.search(r'\d+\.\s+[^0-9]+\s+\d+\.\s+', line):
                    self.add_error(file_path, i, f"Multiple numbered items on same line: {line.strip()[:60]}...")
                
                # Pattern: checklist items on same line
                if line.count('[ ]') > 1 or line.count('[x]') > 1:
                    self.add_error(file_path, i, f"Multiple checklist items on same line: {line.strip()[:60]}...")
                
                # Check for inline content after list markers
                if re.match(r'^\d+\.\s+\*\*[^*]+\*\*\s*-\s*', line):
                    self.add_error(file_path, i, f"Inline content after numbered item: {line.strip()[:60]}...")
                
                # Check for missing line breaks after bold headers
                if line.strip().endswith(':**') and i < len(lines):
                    if i < len(lines) - 1:
                        next_line = lines[i]
                        if next_line.strip() and not next_line.strip().startswith(('-', '*', '#', '1.', '2.', '3.')):
                            self.add_warning(file_path, i, "Bold header should be followed by blank line or list")
    
    def check_bold_formatting(self, content, file_path):
        """Check for incomplete or broken bold markdown patterns"""
        lines = content.split('\n')
        for i, line in enumerate(lines, 1):
            # Check for incomplete bold patterns like **text* (ending with single *)
            if re.search(r'\*\*[^*\n]+\*(?!\*)', line):
                self.add_error(file_path, i, f"Incomplete bold formatting: {line.strip()}")
            
            # Check for double ** patterns that should be single
            if re.search(r'\*\*\*\*', line) and not re.search(r'\*{6,}', line):
                self.add_error(file_path, i, f"Double bold formatting: {line.strip()}")
            
            # Check for broken bold at line endings
            if re.search(r'\*\*[^*]+$', line) and not line.strip().endswith('**'):
                self.add_warning(file_path, i, f"Unclosed bold formatting: {line.strip()}")
    
    def check_list_structure(self, content, file_path):
        """Check overall list structure and formatting"""
        lines = content.split('\n')
        prev_was_list = False
        
        for i, line in enumerate(lines, 1):
            is_list = bool(re.match(r'^\s*[-*]\s+', line) or re.match(r'^\s*\d+\.\s+', line))
            
            # Check for list items without proper spacing
            if is_list:
                # Check indentation consistency
                if re.match(r'^[-*]\s+', line) and not re.match(r'^[-*]\s+', line):
                    self.add_warning(file_path, i, "Bullet list should start at beginning of line")
                
                # Check for missing content after list marker
                if re.match(r'^\s*[-*]\s*$', line) or re.match(r'^\s*\d+\.\s*$', line):
                    self.add_error(file_path, i, "Empty list item")
            
            prev_was_list = is_list
    
    def fix_arena_card_content(self, content):
        """Auto-fix arena card content issues"""
        lines = content.split('\n')
        fixed_lines = []
        in_arena_card = False
        arena_depth = 0
        fixes_count = 0
        
        i = 0
        while i < len(lines):
            line = lines[i]
            
            # Track arena-card state
            if '<div class="arena-card"' in line:
                in_arena_card = True
                arena_depth += 1
                # Add markdown="1" if missing
                if 'markdown="1"' not in line and line.strip().endswith('>'):
                    line = line.replace('>', ' markdown="1">')
                    fixes_count += 1
                fixed_lines.append(line)
                i += 1
                continue
                
            elif '</div>' in line and in_arena_card:
                arena_depth -= 1
                if arena_depth == 0:
                    in_arena_card = False
                fixed_lines.append(line)
                i += 1
                continue
            
            # Process arena-card content
            if in_arena_card and line.strip():
                fixed = False
                
                # Fix Pattern 1: "**Header:** - item1 - item2 - item3"
                if re.match(r'^\*\*[^*]+:\*\*\s*-\s*', line) and ' - ' in line:
                    parts = line.split(' - ')
                    if len(parts) > 1:
                        # First part is the header
                        fixed_lines.append(parts[0].rstrip())
                        # Add blank line after header if next items are lists
                        if parts[1].strip():
                            fixed_lines.append('')
                        # Rest are list items
                        for j in range(1, len(parts)):
                            if parts[j].strip():
                                fixed_lines.append(f"- {parts[j].strip()}")
                        fixes_count += 1
                        fixed = True
                
                # Fix Pattern 2: Running bullet list "- item1 - item2 - item3"
                elif line.startswith('-') and line.count(' - ') >= 1:
                    items = re.split(r'\s+-\s+', line)
                    if len(items) > 1:
                        for item in items:
                            clean_item = item.strip()
                            if clean_item:
                                if not clean_item.startswith('-'):
                                    clean_item = f"- {clean_item}"
                                fixed_lines.append(clean_item)
                        fixes_count += 1
                        fixed = True
                
                # Fix Pattern 3: Bold sections without proper spacing
                elif ':**' in line and ' - ' in line and not line.startswith('-'):
                    match = re.match(r'^(\*\*[^*]+:\*\*)\s*(.+)$', line)
                    if match:
                        fixed_lines.append(match.group(1))
                        fixed_lines.append('')  # Add blank line
                        # Handle the rest which might have list items
                        rest = match.group(2)
                        if rest.startswith('- '):
                            items = rest.split(' - ')
                            for item in items:
                                if item.strip():
                                    fixed_lines.append(f"- {item.strip()}")
                        else:
                            fixed_lines.append(rest)
                        fixes_count += 1
                        fixed = True
                
                # Fix Pattern 4: Numbered lists running together
                elif re.search(r'\d+\.\s+[^0-9]+\s+\d+\.\s+', line):
                    parts = re.split(r'(\d+\.\s+)', line)
                    current_item = ""
                    for part in parts:
                        if re.match(r'\d+\.\s+$', part):
                            if current_item.strip():
                                fixed_lines.append(current_item.strip())
                            current_item = part
                        else:
                            current_item += part
                    if current_item.strip():
                        fixed_lines.append(current_item.strip())
                    fixes_count += 1
                    fixed = True
                
                # Fix Pattern 5: Checklist items on same line
                elif line.count('[ ]') > 1:
                    if ':' in line and not line.startswith('-'):
                        # Handle "Day 1: - [ ] item1 - [ ] item2"
                        prefix, rest = line.split(':', 1)
                        fixed_lines.append(f"{prefix}:")
                        items = re.findall(r'-\s*\[\s*\][^-]+', rest)
                        for item in items:
                            if item.strip():
                                fixed_lines.append(item.strip())
                    else:
                        # Just split items
                        items = re.findall(r'-\s*\[\s*\][^-]+', line)
                        for item in items:
                            if item.strip():
                                fixed_lines.append(item.strip())
                    fixes_count += 1
                    fixed = True
                
                # Fix Pattern 6: Inline content after numbered items
                elif re.match(r'^\d+\.\s+\*\*[^*]+\*\*\s*-\s*', line):
                    match = re.match(r'^(\d+\.\s+\*\*[^*]+\*\*)\s*-\s*(.+)$', line)
                    if match:
                        fixed_lines.append(match.group(1))
                        fixed_lines.append(f"   - {match.group(2)}")
                        fixes_count += 1
                        fixed = True
                
                # Fix double asterisks
                elif '****' in line and not '*****' in line:
                    line = re.sub(r'\*{4}', '**', line)
                    fixes_count += 1
                
                if not fixed:
                    fixed_lines.append(line)
            else:
                # Not in arena card or empty line
                fixed_lines.append(line)
            
            i += 1
        
        self.fixes_applied += fixes_count
        return '\n'.join(fixed_lines)
    
    def check_headers(self, content, file_path):
        """Check header formatting and hierarchy"""
        lines = content.split('\n')
        prev_level = 0
        
        for i, line in enumerate(lines, 1):
            if line.startswith('#'):
                # Count header level
                level = len(line) - len(line.lstrip('#'))
                
                # Check for proper spacing after #
                if not re.match(r'^#{1,6}\s+', line):
                    self.add_error(file_path, i, f"Header missing space after #: {line.strip()}")
                
                # Check header hierarchy (skip too large jumps)
                if prev_level > 0 and level > prev_level + 1:
                    self.add_warning(file_path, i, f"Header level jumped from h{prev_level} to h{level}")
                
                prev_level = level
    
    def check_links(self, content, file_path):
        """Check markdown links formatting"""
        lines = content.split('\n')
        for i, line in enumerate(lines, 1):
            # Check for broken link format
            if re.search(r'\[([^\]]+)\]\([^)]*$', line):
                self.add_error(file_path, i, f"Unclosed link: {line.strip()}")
            
            # Check for links without text
            if re.search(r'\[\]\([^)]+\)', line):
                self.add_warning(file_path, i, f"Link without text: {line.strip()}")
    
    def lint_file(self, file_path, auto_fix=False):
        """Lint a single markdown file with optional auto-fix"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            self.add_error(file_path, 1, f"Could not read file: {e}")
            return
        
        # Apply fixes if requested
        if auto_fix:
            original_content = content
            content = self.fix_arena_card_content(content)
            
            # Apply multiple passes to catch nested issues
            for _ in range(2):
                prev_content = content
                content = self.fix_arena_card_content(content)
                if content == prev_content:
                    break
            
            # Write back if changes were made
            if content != original_content:
                try:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    print(f"✅ Fixed formatting in {file_path}")
                except Exception as e:
                    self.add_error(file_path, 1, f"Could not write fixed file: {e}")
        
        # Run all checks on the (potentially fixed) content
        self.check_headers(content, file_path)
        self.check_bold_formatting(content, file_path)
        self.check_list_structure(content, file_path)
        self.check_links(content, file_path)
        self.check_arena_card_lists(content, file_path)
        
        self.file_count += 1
    
    def lint_directory(self, directory, auto_fix=False):
        """Lint all markdown files in a directory"""
        md_files = glob.glob(os.path.join(directory, '**/*.md'), recursive=True)
        
        for file_path in md_files:
            self.lint_file(file_path, auto_fix)
    
    def print_results(self):
        """Print linting results"""
        print(f"\n📋 Final Markdown Linting Results")
        print(f"Files checked: {self.file_count}")
        print(f"Auto-fixes applied: {self.fixes_applied}")
        print(f"Errors: {len(self.errors)}")
        print(f"Warnings: {len(self.warnings)}")
        
        if self.errors:
            print(f"\n❌ ERRORS ({len(self.errors)}):")
            for error in self.errors[:30]:  # Show more errors
                print(f"  {error}")
            if len(self.errors) > 30:
                print(f"  ... and {len(self.errors) - 30} more errors")
        
        if self.warnings:
            print(f"\n⚠️  WARNINGS ({len(self.warnings)}):")
            for warning in self.warnings[:20]:
                print(f"  {warning}")
            if len(self.warnings) > 20:
                print(f"  ... and {len(self.warnings) - 20} more warnings")
        
        if not self.errors and not self.warnings:
            print("\n✅ All files passed final linting!")
        
        return len(self.errors)

def main():
    """Main entry point"""
    auto_fix = '--fix' in sys.argv
    
    # Parse arguments
    args = [arg for arg in sys.argv[1:] if arg != '--fix']
    target = args[0] if args else 'docs'
    
    linter = FinalMarkdownLinter()
    
    if auto_fix:
        print("🔧 Running final markdown linter with auto-fix enabled...")
    else:
        print("🔍 Running final markdown linter...")
    
    if os.path.isfile(target):
        linter.lint_file(target, auto_fix)
    elif os.path.isdir(target):
        linter.lint_directory(target, auto_fix)
    else:
        print(f"Error: {target} is not a valid file or directory")
        sys.exit(1)
    
    error_count = linter.print_results()
    
    # Exit with error code if there are errors (but not if we just applied fixes)
    if auto_fix and linter.fixes_applied > 0:
        print(f"\n💡 Run again without --fix to verify all issues are resolved")
        sys.exit(0)
    else:
        sys.exit(1 if error_count > 0 else 0)

if __name__ == "__main__":
    main()