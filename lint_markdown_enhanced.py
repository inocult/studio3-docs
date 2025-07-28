#!/usr/bin/env python3
"""
Enhanced Studio3 Markdown Linter with Arena-Card specific rules and auto-fix capability
"""

import os
import re
import sys
import glob
import yaml
from pathlib import Path

class EnhancedMarkdownLinter:
    def __init__(self):
        self.errors = []
        self.warnings = []
        self.file_count = 0
        self.fixes_applied = 0
        
    def add_error(self, file_path, line_num, message):
        self.errors.append(f"{file_path}:{line_num}: ERROR: {message}")
        
    def add_warning(self, file_path, line_num, message):
        self.warnings.append(f"{file_path}:{line_num}: WARNING: {message}")
    
    def check_bold_formatting(self, content, file_path):
        """Check for incomplete bold markdown patterns"""
        lines = content.split('\n')
        for i, line in enumerate(lines, 1):
            # Check for truly incomplete bold patterns like **text* (ending with single *)
            if re.search(r'\*\*[^*\n]+\*(?!\*)', line):
                self.add_error(file_path, i, f"Incomplete bold formatting: {line.strip()}")
            
            # Check for orphaned ** at start of numbered lists
            if re.match(r'^\*\*\d+\.', line):
                self.add_error(file_path, i, f"Broken numbered list: {line.strip()}")
            
            # Check for double ** patterns that should be single
            if re.search(r'\*\*([^*\n]+)\*\*\*\*', line):
                self.add_error(file_path, i, f"Double bold formatting: {line.strip()}")
    
    def check_list_formatting(self, content, file_path):
        """Check for broken list formatting"""
        lines = content.split('\n')
        for i, line in enumerate(lines, 1):
            # Check for orphaned ** at start of lines
            if re.match(r'^\*\*\d+\.', line):
                self.add_error(file_path, i, f"Broken numbered list formatting: {line.strip()}")
            
            # Check for broken bullet lists with ** markers
            if re.match(r'^\*\*(\s|$)', line):
                self.add_error(file_path, i, f"Broken bullet list formatting: {line.strip()}")
    
    def check_arena_cards_enhanced(self, content, file_path):
        """Enhanced arena-card checking with specific rules for lists and formatting"""
        lines = content.split('\n')
        in_arena_card = False
        arena_start_line = 0
        
        for i, line in enumerate(lines, 1):
            if '<div class="arena-card"' in line:
                in_arena_card = True
                arena_start_line = i
                # Check for markdown="1" attribute
                if 'markdown="1"' not in line and line.strip().endswith('>'):
                    self.add_warning(file_path, i, "Arena card missing markdown=\"1\" attribute")
            
            elif '</div>' in line and in_arena_card:
                in_arena_card = False
                arena_start_line = 0
            
            elif in_arena_card:
                # Check for running checklist items (multiple checkbox items on same line)
                if re.search(r'\[\s*\]\s*[^-\n]+\s*-\s*\[\s*\]', line):
                    self.add_error(file_path, i, f"Arena card checklist items running together: {line.strip()}")
                
                # Check for running bullet list items (multiple - items on same line)
                bullet_matches = re.findall(r'-\s*[^-\n]+(?=\s*-)', line)
                if len(bullet_matches) > 0 and ' - ' in line:
                    # Count bullet points on the line
                    bullet_count = len(re.findall(r'-\s*[^-]+', line))
                    if bullet_count > 1:
                        self.add_error(file_path, i, f"Arena card bullet list items running together: {line.strip()}")
                
                # Check for running numbered list items (multiple numbered items on same line)
                numbered_matches = re.findall(r'\d+\.\s*[^0-9\n]+(?=\s*\d+\.)', line)
                if len(numbered_matches) > 0:
                    self.add_error(file_path, i, f"Arena card numbered list items running together: {line.strip()}")
                
                # Check for broken bold patterns in arena cards
                if re.search(r'\*\*[^*]+$', line) and not line.strip().endswith('**'):
                    self.add_warning(file_path, i, f"Potential unrendered bold in arena card: {line.strip()}")
                
                # Check for proper section headers in arena cards
                if line.strip().endswith(':') and not line.strip().startswith(('**', '-', '#')):
                    self.add_warning(file_path, i, f"Arena card section header should be bold: {line.strip()}")
    
    def fix_arena_card_formatting(self, content):
        """Auto-fix arena card formatting issues"""
        lines = content.split('\n')
        fixed_lines = []
        in_arena_card = False
        fixes_count = 0
        
        for line in lines:
            original_line = line
            
            if '<div class="arena-card"' in line:
                in_arena_card = True
            elif '</div>' in line and in_arena_card:
                in_arena_card = False
            elif in_arena_card:
                # Fix running checklist items
                # Pattern: Day 1: - [ ] item1 - [ ] item2 - [ ] item3
                if re.search(r'\[\s*\]\s*[^-\n]+\s*-\s*\[\s*\]', line):
                    # Split on checkbox patterns and rebuild with proper line breaks
                    parts = re.split(r'(\s*-\s*\[\s*\][^\-]+?)(?=\s*-\s*\[)', line)
                    if len(parts) > 1:
                        new_lines = []
                        for part in parts:
                            if part.strip() and '[ ]' in part:
                                # Clean up the checkbox item
                                clean_part = re.sub(r'^(\s*-\s*)', '- ', part.strip())
                                new_lines.append(clean_part)
                            elif part.strip() and not '[ ]' in part:
                                # This might be the prefix (like "Day 1:")
                                new_lines.append(part.strip())
                        
                        if len(new_lines) > 1:
                            line = '\n'.join(new_lines)
                            fixes_count += 1
                
                # Fix running bullet list items
                # Pattern: - item1 - item2 - item3
                elif ' - ' in line and not line.strip().startswith('#'):
                    bullet_parts = re.split(r'\s*-\s*', line)
                    if len(bullet_parts) > 2:  # More than just the part before first -
                        new_bullet_lines = []
                        for i, part in enumerate(bullet_parts):
                            if part.strip():
                                if i == 0:
                                    # First part might not be a list item
                                    if ':' in part or part.strip().endswith(':'):
                                        new_bullet_lines.append(part.strip())
                                    else:
                                        new_bullet_lines.append(f"- {part.strip()}")
                                else:
                                    new_bullet_lines.append(f"- {part.strip()}")
                        
                        if len(new_bullet_lines) > 1:
                            line = '\n'.join(new_bullet_lines)
                            fixes_count += 1
                
                # Fix running numbered list items
                # Pattern: 1. item1 2. item2 3. item3
                elif re.search(r'\d+\.\s*[^0-9\n]+\s*\d+\.', line):
                    # Split on numbered patterns
                    numbered_parts = re.split(r'(\d+\.\s*)', line)
                    new_numbered_lines = []
                    current_item = ""
                    
                    for part in numbered_parts:
                        if re.match(r'\d+\.\s*$', part):
                            if current_item.strip():
                                new_numbered_lines.append(current_item.strip())
                            current_item = part
                        elif part.strip():
                            current_item += part
                            # Check if this part ends an item (contains another number)
                            if re.search(r'^[^0-9]*(?=\s*\d+\.)', part):
                                content_before_next = re.split(r'(?=\s*\d+\.)', part)[0]
                                current_item = current_item.replace(part, content_before_next)
                                new_numbered_lines.append(current_item.strip())
                                # Start new item with the remaining part
                                remaining = part[len(content_before_next):].strip()
                                if remaining:
                                    current_item = remaining
                                else:
                                    current_item = ""
                    
                    if current_item.strip():
                        new_numbered_lines.append(current_item.strip())
                    
                    if len(new_numbered_lines) > 1:
                        line = '\n'.join(new_numbered_lines)
                        fixes_count += 1
                
                # Fix section headers that should be bold
                if line.strip().endswith(':') and not line.strip().startswith(('**', '-', '#', '<')):
                    if not re.search(r'\*\*.*\*\*:', line):
                        # Make the section header bold
                        line = f"**{line.strip()}**"
                        fixes_count += 1
            
            # Split multi-line fixes properly
            if '\n' in line:
                fixed_lines.extend(line.split('\n'))
            else:
                fixed_lines.append(line)
        
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
    
    def check_special_patterns(self, content, file_path):
        """Check for Studio3-specific patterns"""
        lines = content.split('\n')
        for i, line in enumerate(lines, 1):
            # Check for $STUDIO instead of $SIGNAL
            if '$STUDIO' in line:
                self.add_error(file_path, i, "Use $SIGNAL instead of $STUDIO")
    
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
            content = self.fix_arena_card_formatting(content)
            
            # Write back if changes were made
            if content != original_content:
                try:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    print(f"✅ Fixed arena-card formatting in {file_path}")
                except Exception as e:
                    self.add_error(file_path, 1, f"Could not write fixed file: {e}")
        
        # Run all checks on the (potentially fixed) content
        self.check_headers(content, file_path)
        self.check_bold_formatting(content, file_path)
        self.check_list_formatting(content, file_path)
        self.check_links(content, file_path)
        self.check_arena_cards_enhanced(content, file_path)
        self.check_special_patterns(content, file_path)
        
        self.file_count += 1
    
    def lint_directory(self, directory, auto_fix=False):
        """Lint all markdown files in a directory"""
        md_files = glob.glob(os.path.join(directory, '**/*.md'), recursive=True)
        
        for file_path in md_files:
            self.lint_file(file_path, auto_fix)
    
    def print_results(self):
        """Print linting results"""
        print(f"\n📋 Enhanced Markdown Linting Results")
        print(f"Files checked: {self.file_count}")
        print(f"Auto-fixes applied: {self.fixes_applied}")
        print(f"Errors: {len(self.errors)}")
        print(f"Warnings: {len(self.warnings)}")
        
        if self.errors:
            print(f"\n❌ ERRORS ({len(self.errors)}):")
            for error in self.errors[:20]:  # Limit output
                print(f"  {error}")
            if len(self.errors) > 20:
                print(f"  ... and {len(self.errors) - 20} more errors")
        
        if self.warnings:
            print(f"\n⚠️  WARNINGS ({len(self.warnings)}):")
            for warning in self.warnings[:10]:  # Limit output
                print(f"  {warning}")
            if len(self.warnings) > 10:
                print(f"  ... and {len(self.warnings) - 10} more warnings")
        
        if not self.errors and not self.warnings:
            print("\n✅ All files passed enhanced linting!")
        
        return len(self.errors)

def main():
    """Main entry point"""
    auto_fix = '--fix' in sys.argv
    
    if len(sys.argv) > 1:
        target = sys.argv[1] if sys.argv[1] != '--fix' else 'docs'
        if len(sys.argv) > 2 and sys.argv[1] == '--fix':
            target = sys.argv[2]
    else:
        target = 'docs'
    
    linter = EnhancedMarkdownLinter()
    
    if auto_fix:
        print("🔧 Running enhanced markdown linter with auto-fix enabled...")
    else:
        print("🔍 Running enhanced markdown linter...")
    
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