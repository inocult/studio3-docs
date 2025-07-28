#!/usr/bin/env python3
"""
Studio3 Markdown Linter - Comprehensive markdown validation
Catches common markdown rendering issues before they reach production
"""

import os
import re
import sys
import glob
import yaml
from pathlib import Path

class MarkdownLinter:
    def __init__(self):
        self.errors = []
        self.warnings = []
        self.file_count = 0
        
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
    
    def check_arena_cards(self, content, file_path):
        """Check arena-card div formatting"""
        lines = content.split('\n')
        in_arena_card = False
        
        for i, line in enumerate(lines, 1):
            if '<div class="arena-card"' in line:
                in_arena_card = True
                # Check for markdown="1" attribute
                if 'markdown="1"' not in line and line.strip().endswith('>'):
                    self.add_warning(file_path, i, "Arena card missing markdown=\"1\" attribute")
            
            elif '</div>' in line and in_arena_card:
                in_arena_card = False
            
            elif in_arena_card:
                # Check for potential rendering issues in arena cards
                if re.search(r'\*\*[^*]+$', line):
                    self.add_warning(file_path, i, f"Potential unrendered bold in arena card: {line.strip()}")
    
    def check_yaml_frontmatter(self, content, file_path):
        """Check YAML frontmatter if present"""
        if content.startswith('---\n'):
            try:
                end_idx = content.find('\n---\n', 4)
                if end_idx != -1:
                    yaml_content = content[4:end_idx]
                    yaml.safe_load(yaml_content)
            except yaml.YAMLError as e:
                self.add_error(file_path, 1, f"Invalid YAML frontmatter: {e}")
    
    def check_line_endings(self, content, file_path):
        """Check for consistent line endings and trailing whitespace"""
        lines = content.split('\n')
        for i, line in enumerate(lines, 1):
            # Check for trailing whitespace (except intentional 2-space line breaks)
            if line.endswith(' ') and not line.endswith('  '):
                self.add_warning(file_path, i, "Trailing whitespace")
            
            # Check for Windows line endings
            if '\r' in line:
                self.add_warning(file_path, i, "Windows line endings detected")
    
    def check_special_patterns(self, content, file_path):
        """Check for Studio3-specific patterns"""
        lines = content.split('\n')
        for i, line in enumerate(lines, 1):
            # Check for $STUDIO instead of $SIGNAL
            if '$STUDIO' in line:
                self.add_error(file_path, i, "Use $SIGNAL instead of $STUDIO")
            
            # Check for missing closing asterisks in lists
            if re.search(r'^[\s]*[-*]\s+\*\*[^*]+$', line):
                self.add_error(file_path, i, f"Unclosed bold in list item: {line.strip()}")
            
            # Check for missing colons after bold headings
            if re.search(r'\*\*[^*:]+$', line) and not re.search(r'\*\*[^*]+\*\*', line):
                if any(word in line.lower() for word in ['traditional', 'studio3', 'if you', 'clear']):
                    self.add_error(file_path, i, f"Missing colon after bold heading: {line.strip()}")
    
    def lint_file(self, file_path):
        """Lint a single markdown file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            self.add_error(file_path, 1, f"Could not read file: {e}")
            return
        
        # Run all checks
        self.check_yaml_frontmatter(content, file_path)
        self.check_headers(content, file_path)
        self.check_bold_formatting(content, file_path)
        self.check_list_formatting(content, file_path)
        self.check_links(content, file_path)
        self.check_arena_cards(content, file_path)
        self.check_line_endings(content, file_path)
        self.check_special_patterns(content, file_path)
        
        self.file_count += 1
    
    def lint_directory(self, directory):
        """Lint all markdown files in a directory"""
        md_files = glob.glob(os.path.join(directory, '**/*.md'), recursive=True)
        
        for file_path in md_files:
            self.lint_file(file_path)
    
    def print_results(self):
        """Print linting results"""
        print(f"\n📋 Markdown Linting Results")
        print(f"Files checked: {self.file_count}")
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
            print("\n✅ All files passed linting!")
        
        return len(self.errors)

def main():
    """Main entry point"""
    if len(sys.argv) > 1:
        target = sys.argv[1]
    else:
        target = 'docs'
    
    linter = MarkdownLinter()
    
    if os.path.isfile(target):
        linter.lint_file(target)
    elif os.path.isdir(target):
        linter.lint_directory(target)
    else:
        print(f"Error: {target} is not a valid file or directory")
        sys.exit(1)
    
    error_count = linter.print_results()
    
    # Exit with error code if there are errors
    sys.exit(1 if error_count > 0 else 0)

if __name__ == "__main__":
    main()