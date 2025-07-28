#!/usr/bin/env python3
"""
Strict markdown linter that catches ALL formatting issues
Including malformed lists, broken bold patterns, and spacing issues
"""

import os
import re
import sys
import glob
from pathlib import Path

class StrictMarkdownLinter:
    def __init__(self):
        self.errors = []
        self.warnings = []
        self.file_count = 0
        
    def add_error(self, file_path, line_num, message, line_content=""):
        preview = f" -> {line_content.strip()[:60]}..." if line_content else ""
        self.errors.append(f"{file_path}:{line_num}: ERROR: {message}{preview}")
        
    def add_warning(self, file_path, line_num, message, line_content=""):
        preview = f" -> {line_content.strip()[:60]}..." if line_content else ""
        self.warnings.append(f"{file_path}:{line_num}: WARNING: {message}{preview}")
    
    def check_list_item_spacing(self, content, file_path):
        """Check for proper list item formatting and spacing"""
        lines = content.split('\n')
        
        for i, line in enumerate(lines, 1):
            # Check for numbered lists without proper format
            # Pattern: 1. **text** content (should have newline after number)
            if re.match(r'^\d+\.\s*\*\*[^*]+\*\*\s+\S', line):
                self.add_error(file_path, i, "Numbered list with inline bold content", line)
            
            # Check for dash directly attached to asterisks: -**text
            if re.match(r'^-\*\*', line):
                self.add_error(file_path, i, "Dash directly attached to bold markers", line)
            
            # Check for list items with extra asterisks at line end
            if re.match(r'^[-*]\s+.*\*\*\s*$', line) and not re.match(r'^[-*]\s+.*\*\*[^*]+\*\*\s*$', line):
                self.add_error(file_path, i, "List item with trailing asterisks", line)
            
            # Check for multiple list items on one line
            if re.match(r'^[-*]\s+', line) and line.count(' - ') >= 1:
                self.add_error(file_path, i, "Multiple list items on single line", line)
    
    def check_bold_patterns(self, content, file_path):
        """Check for malformed bold patterns"""
        lines = content.split('\n')
        
        for i, line in enumerate(lines, 1):
            # Check for ****text** pattern
            if re.search(r'\*{4}[^*]+\*{2}', line):
                self.add_error(file_path, i, "Four asterisks followed by two", line)
            
            # Check for **text**** pattern
            if re.search(r'\*{2}[^*]+\*{4}', line):
                self.add_error(file_path, i, "Two asterisks followed by four", line)
            
            # Check for incomplete bold: **text*
            if re.search(r'\*\*[^*\n]+\*(?!\*)', line):
                self.add_error(file_path, i, "Incomplete bold formatting", line)
            
            # Check for bold text with content and trailing **
            # Pattern: **text** some content**
            if re.search(r'\*\*[^*]+\*\*[^*]+\*\*\s*$', line):
                self.add_error(file_path, i, "Bold text with trailing asterisks", line)
            
            # Check for -** pattern (dash followed by asterisks)
            if re.search(r'-\*{2,}', line):
                self.add_error(file_path, i, "Dash followed by asterisks without space", line)
    
    def check_info_blocks(self, content, file_path):
        """Check for malformed info/warning/tip blocks"""
        lines = content.split('\n')
        in_block = False
        block_start = 0
        
        for i, line in enumerate(lines, 1):
            if line.strip().startswith('!!!'):
                in_block = True
                block_start = i
                # Check if next line is properly indented
                if i < len(lines):
                    next_line = lines[i] if i < len(lines) else ""
                    if next_line.strip() and not next_line.startswith('    '):
                        self.add_warning(file_path, i+1, "Content after !!! block should be indented with 4 spaces", next_line)
            
            elif in_block and line.strip() and not line.startswith('    '):
                # Block ended
                in_block = False
            
            # Check for malformed list items in blocks
            if in_block and re.match(r'^\s*-\s*\*\*.*\*\*\s*:\s*[^*]+\*\*', line):
                self.add_error(file_path, i, "Malformed list item in info block", line)
    
    def check_header_list_patterns(self, content, file_path):
        """Check for headers followed by improper list formatting"""
        lines = content.split('\n')
        
        for i, line in enumerate(lines, 1):
            # Check for pattern: **text:** 1.**text**
            if re.search(r'\*\*[^*]+:\*\*\s*\d+\.\s*\*\*', line):
                self.add_error(file_path, i, "Header with inline numbered list", line)
            
            # Check for pattern: **Level 1: text
            if re.match(r'^\*\*[^*]+:\s*\w+', line) and not line.endswith('**'):
                self.add_error(file_path, i, "Bold header not properly closed", line)
            
            # Check for list continuation patterns
            # Pattern: - ** text (should be - **text**)
            if re.match(r'^-\s+\*\*\s+\w+', line):
                self.add_error(file_path, i, "Space between asterisks in list item", line)
    
    def check_nested_list_spacing(self, content, file_path):
        """Check for proper nested list spacing"""
        lines = content.split('\n')
        
        for i, line in enumerate(lines, 1):
            # Check for numbered list followed by dash without proper indentation
            if i > 0 and re.match(r'^\d+\.\s+', lines[i-1]) and re.match(r'^-\s+', line):
                self.add_error(file_path, i, "Dash list should be indented under numbered list", line)
            
            # Check for improper continuation
            # Pattern: text\n- item (missing blank line or indentation)
            if i > 0 and lines[i-1].strip() and not lines[i-1].strip().endswith(':') and re.match(r'^-\s+', line):
                if not re.match(r'^[-*\d]', lines[i-1]):
                    self.add_warning(file_path, i, "List starting without blank line or after colon", line)
    
    def check_colon_patterns(self, content, file_path):
        """Check for colons followed by improper formatting"""
        lines = content.split('\n')
        
        for i, line in enumerate(lines, 1):
            # Pattern: text: Clear, specific commitments**
            if re.search(r':\s*[A-Z][^*\n]+\*\*\s*$', line) and '**' in line:
                self.add_error(file_path, i, "Text after colon with trailing asterisks", line)
            
            # Pattern: ** text:** (space before closing asterisks)
            if re.search(r'\*\*\s+[^*]+\s*:\s*\*\*', line):
                self.add_error(file_path, i, "Space inside bold markers", line)
    
    def check_complex_patterns(self, content, file_path):
        """Check for complex malformed patterns"""
        lines = content.split('\n')
        
        for i, line in enumerate(lines, 1):
            # Pattern: - **text** - text**
            if re.match(r'^-\s*\*\*[^*]+\*\*.*-.*\*\*\s*$', line):
                self.add_error(file_path, i, "List item with multiple dashes and trailing asterisks", line)
            
            # Pattern: **Example:**: text**
            if re.search(r'\*\*[^*]+:\*\*:\s*[^*]+\*\*', line):
                self.add_error(file_path, i, "Double colon pattern with trailing asterisks", line)
            
            # Check for inline numbered lists in a paragraph
            if line.count('. **') >= 2 and not line.startswith((' ', '\t')):
                self.add_error(file_path, i, "Multiple numbered items on single line", line)
    
    def check_table_formatting(self, content, file_path):
        """Check for proper table formatting"""
        lines = content.split('\n')
        in_table = False
        
        for i, line in enumerate(lines, 1):
            if '|' in line and line.count('|') >= 2:
                # Check for malformed bold in tables
                if re.search(r'\|[^|]*\*\*[^*|]+\s+\|', line):
                    self.add_warning(file_path, i, "Incomplete bold in table cell", line)
                
                # Check for proper table separator
                if re.match(r'^\|[\s-]+\|', line):
                    in_table = True
                elif in_table and not line.strip().startswith('|'):
                    in_table = False
    
    def check_paragraph_list_mixing(self, content, file_path):
        """Check for paragraphs that mix with list formatting"""
        lines = content.split('\n')
        
        for i, line in enumerate(lines, 1):
            # Check for pattern: word- **text (missing space before dash)
            if re.search(r'[a-zA-Z]-\s*\*\*', line):
                self.add_error(file_path, i, "Word followed by dash without space", line)
            
            # Check for mid-paragraph list markers
            if not line.startswith(('-', '*', ' ', '\t')) and ' - ' in line:
                # This might be intentional, but worth checking
                if line.count(' - ') > 1:
                    self.add_warning(file_path, i, "Multiple dashes in paragraph (possible list items)", line)
    
    def lint_file(self, file_path):
        """Lint a single markdown file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            self.add_error(file_path, 1, f"Could not read file: {e}")
            return
        
        # Run all checks
        self.check_list_item_spacing(content, file_path)
        self.check_bold_patterns(content, file_path)
        self.check_info_blocks(content, file_path)
        self.check_header_list_patterns(content, file_path)
        self.check_nested_list_spacing(content, file_path)
        self.check_colon_patterns(content, file_path)
        self.check_complex_patterns(content, file_path)
        self.check_table_formatting(content, file_path)
        self.check_paragraph_list_mixing(content, file_path)
        
        self.file_count += 1
    
    def lint_directory(self, directory):
        """Lint all markdown files in a directory"""
        md_files = glob.glob(os.path.join(directory, '**/*.md'), recursive=True)
        
        for file_path in sorted(md_files):
            self.lint_file(file_path)
    
    def print_results(self):
        """Print linting results"""
        print(f"\n📋 Strict Markdown Linting Results")
        print(f"Files checked: {self.file_count}")
        print(f"Errors: {len(self.errors)}")
        print(f"Warnings: {len(self.warnings)}")
        
        if self.errors:
            print(f"\n❌ ERRORS ({len(self.errors)}):")
            # Group errors by type
            error_types = {}
            for error in self.errors:
                # Extract error type
                if "Dash directly attached" in error:
                    key = "Dash attachment issues"
                elif "trailing asterisks" in error:
                    key = "Trailing asterisk issues"
                elif "Four asterisks" in error or "Two asterisks followed by four" in error:
                    key = "Multiple asterisk issues"
                elif "Multiple list items" in error or "Multiple numbered items" in error:
                    key = "Multiple items on line"
                elif "inline" in error.lower():
                    key = "Inline content issues"
                elif "bold" in error.lower():
                    key = "Bold formatting issues"
                elif "list" in error.lower():
                    key = "List formatting issues"
                else:
                    key = "Other formatting issues"
                
                if key not in error_types:
                    error_types[key] = []
                error_types[key].append(error)
            
            # Show grouped errors
            for error_type, errors in sorted(error_types.items()):
                print(f"\n  {error_type} ({len(errors)} instances):")
                for error in errors[:10]:  # Show first 10 of each type
                    print(f"    {error}")
                if len(errors) > 10:
                    print(f"    ... and {len(errors) - 10} more")
        
        if self.warnings:
            print(f"\n⚠️  WARNINGS ({len(self.warnings)}):")
            for warning in self.warnings[:20]:
                print(f"  {warning}")
            if len(self.warnings) > 20:
                print(f"  ... and {len(self.warnings) - 20} more warnings")
        
        if not self.errors and not self.warnings:
            print("\n✅ All files passed strict linting!")
        
        return len(self.errors)

def main():
    """Main entry point"""
    # Parse arguments
    args = sys.argv[1:]
    target = args[0] if args else 'docs'
    
    linter = StrictMarkdownLinter()
    
    print("🔍 Running STRICT markdown linter...")
    print("Checking for:")
    print("  - Dash directly attached to bold markers (-**)")
    print("  - Multiple asterisks (****text**)")
    print("  - Trailing asterisks (**text** extra**)")
    print("  - Inline list items")
    print("  - Malformed info blocks")
    print("  - Mixed paragraph/list formatting")
    print("  - And many more patterns...")
    
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