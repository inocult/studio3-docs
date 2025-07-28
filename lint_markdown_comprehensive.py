#!/usr/bin/env python3
"""
Comprehensive markdown linter that catches ALL formatting issues
Including spacing, list formatting, table placement, and more
"""

import os
import re
import sys
from pathlib import Path

class ComprehensiveMarkdownLinter:
    def __init__(self):
        self.errors = []
        self.warnings = []
        self.file_count = 0
        
    def add_error(self, file_path, line_num, message, line_content="", suggestion=""):
        preview = f" -> {line_content.strip()[:60]}..." if line_content else ""
        sugg = f"\n     Suggestion: {suggestion}" if suggestion else ""
        self.errors.append(f"{file_path}:{line_num}: ERROR: {message}{preview}{sugg}")
        
    def add_warning(self, file_path, line_num, message, line_content="", suggestion=""):
        preview = f" -> {line_content.strip()[:60]}..." if line_content else ""
        sugg = f"\n     Suggestion: {suggestion}" if suggestion else ""
        self.warnings.append(f"{file_path}:{line_num}: WARNING: {message}{preview}{sugg}")
    
    def check_spacing_issues(self, lines, file_path):
        """Check for spacing issues around punctuation and formatting"""
        for i, line in enumerate(lines, 1):
            # Check for space before colon in bold text
            if re.search(r'\*\*[^*]+\*\*\s+:', line):
                self.add_error(file_path, i, "Space between bold text and colon", line,
                             "Remove space: **text**: not **text** :")
            
            # Check for missing space after colon
            if re.search(r':[^\s\n]', line) and not re.search(r':\d+|:\/\/|:\w+:', line):
                # Exclude URLs, times, and emoji patterns
                if not re.search(r'https?:|mailto:|[0-9]{1,2}:[0-9]{2}|:\w+:', line):
                    self.add_error(file_path, i, "Missing space after colon", line,
                                 "Add space after colon")
            
            # Check for table immediately after text without blank line
            if '|' in line and i > 1 and lines[i-2].strip() and not lines[i-2].strip().startswith('|'):
                if line.count('|') >= 3:  # Likely a table
                    self.add_error(file_path, i, "Table should have blank line before it", line,
                                 "Add blank line before table")
            
            # Check for heading immediately after text without blank line
            if re.match(r'^#{1,6}\s+', line) and i > 1 and lines[i-2].strip():
                if not lines[i-2].startswith('#'):
                    self.add_error(file_path, i, "Heading should have blank line before it", line,
                                 "Add blank line before heading")
    
    def check_list_formatting(self, lines, file_path):
        """Check for list formatting issues"""
        for i, line in enumerate(lines, 1):
            # Check for broken bold in lists
            if re.match(r'^[-*]\s+\*\*\s+\w', line):
                self.add_error(file_path, i, "Space inside bold markers in list", line,
                             "Fix: - **text** not - ** text")
            
            # Check for list with colon but content on same line
            if re.match(r'^[-*]\s+.*:\s*\w', line) and not line.endswith(':'):
                self.add_warning(file_path, i, "List item with colon should end with colon only", line,
                               "Move content after colon to next line")
            
            # Check for numbered list formatting issues
            if re.match(r'^\d+\.\s+\*\*[^*]+\*\*\s+\w', line):
                self.add_error(file_path, i, "Content after bold in numbered list", line,
                             "Move content to next line or remove bold")
            
            # Check for inconsistent list markers
            if re.match(r'^[-*]\s+', line):
                # Check if previous list items use different marker
                for j in range(max(0, i-5), i-1):
                    if j < len(lines) and re.match(r'^[-*]\s+', lines[j]):
                        prev_marker = lines[j][0]
                        curr_marker = line[0]
                        if prev_marker != curr_marker and lines[j-1].strip() != '':
                            self.add_warning(file_path, i, f"Inconsistent list markers: '{prev_marker}' vs '{curr_marker}'", line)
                            break
    
    def check_bold_patterns(self, lines, file_path):
        """Check for malformed bold patterns"""
        for i, line in enumerate(lines, 1):
            # Check for incomplete bold markers
            bold_count = line.count('**')
            if bold_count % 2 != 0:
                self.add_error(file_path, i, "Odd number of ** markers", line,
                             "Ensure all bold text is properly closed")
            
            # Check for bold with trailing content
            if re.search(r'\*\*[^*]+\*\*[^:\s,\.!?\])}]', line):
                # Allow some punctuation after bold
                self.add_warning(file_path, i, "Content immediately after bold text", line,
                               "Consider adding space or punctuation")
            
            # Check for broken multi-line bold attempts
            if line.strip().endswith('**') and i < len(lines) and lines[i].strip().startswith('**'):
                self.add_error(file_path, i, "Bold text split across lines", line,
                             "Keep bold text on single line")
    
    def check_line_continuity(self, lines, file_path):
        """Check for text that should be on new lines"""
        for i, line in enumerate(lines, 1):
            # Check for multiple headers on same line
            if line.count('**##') > 0 or line.count('**###') > 0:
                self.add_error(file_path, i, "Header marker inside or after bold text", line,
                             "Put header on new line")
            
            # Check for text continuing after what should be a header
            if re.search(r'\*\*[^*]+\*\*\s*#+\s+\w', line):
                self.add_error(file_path, i, "Header continues on same line as previous content", line,
                             "Put header on new line")
            
            # Check for missing line break indicators
            if len(line) > 100 and '**' in line and line.count('**') >= 4:
                self.add_warning(file_path, i, "Very long line with multiple bold sections", line,
                               "Consider breaking into multiple lines")
    
    def check_markdown_in_divs(self, lines, file_path):
        """Check for markdown="1" in arena-card and other divs"""
        in_div = False
        div_line = 0
        
        for i, line in enumerate(lines, 1):
            if '<div class="arena-card"' in line or '<div class="grid' in line:
                in_div = True
                div_line = i
                if 'markdown="1"' not in line:
                    self.add_error(file_path, i, "Missing markdown=\"1\" in div", line,
                                 "Add markdown=\"1\" to enable markdown processing")
            elif '</div>' in line and in_div:
                in_div = False
    
    def check_specific_patterns(self, lines, file_path):
        """Check for specific problematic patterns found in requirements.md"""
        for i, line in enumerate(lines, 1):
            # Pattern: **text** : (space before colon)
            if re.search(r'\*\*[^*]+\*\*\s+:', line):
                self.add_error(file_path, i, "Space between bold text and colon", line,
                             "Remove space: **text**: not **text** :")
            
            # Pattern: - ** text (space after opening bold)
            if re.search(r'^[-*]\s+\*\*\s+', line):
                self.add_error(file_path, i, "Space after opening bold marker", line,
                             "Fix: - **text not - ** text")
            
            # Pattern: text** without opening
            if re.search(r'[^\*]\*\*$', line) and line.count('**') % 2 != 0:
                self.add_error(file_path, i, "Closing bold without opening", line,
                             "Add opening ** marker")
            
            # Pattern: **text**content** (missing space)
            if re.search(r'\*\*[^*]+\*\*[^\s*][^*]*\*\*', line):
                self.add_error(file_path, i, "Missing space between bold sections", line,
                             "Add space between bold sections")
            
            # Pattern: numbered list with content on same line as bold
            if re.match(r'^\d+\.\s+\*\*[^*]+\*\*\s+\(', line):
                self.add_warning(file_path, i, "Content after bold in numbered list", line,
                               "Consider moving content to next line")
    
    def check_indentation(self, lines, file_path):
        """Check for proper indentation in lists and blocks"""
        list_stack = []  # Track list levels
        
        for i, line in enumerate(lines, 1):
            # Count leading spaces
            stripped = line.lstrip()
            if not stripped:
                continue
                
            indent = len(line) - len(stripped)
            
            # Check list indentation
            if re.match(r'^[-*]\s+', stripped):
                expected_indent = len(list_stack) * 2
                if indent != expected_indent and list_stack:
                    self.add_warning(file_path, i, f"Inconsistent list indentation. Expected {expected_indent}, got {indent}", line)
                
                # Update stack
                if not list_stack or indent > list_stack[-1]:
                    list_stack.append(indent)
                elif indent < list_stack[-1]:
                    while list_stack and indent < list_stack[-1]:
                        list_stack.pop()
            elif not line.strip().startswith('-') and not line.strip().startswith('*'):
                # Not a list item, reset stack if not indented continuation
                if indent == 0:
                    list_stack = []
    
    def check_file_structure(self, content, file_path):
        """Check overall file structure issues"""
        lines = content.split('\n')
        
        # Check for missing title
        if not lines or not lines[0].startswith('# '):
            self.add_error(file_path, 1, "File should start with # heading")
        
        # Check for multiple consecutive blank lines
        blank_count = 0
        for i, line in enumerate(lines, 1):
            if not line.strip():
                blank_count += 1
                if blank_count > 2:
                    self.add_warning(file_path, i, "Multiple consecutive blank lines")
            else:
                blank_count = 0
        
        # Check for missing final newline
        if content and not content.endswith('\n'):
            self.add_warning(file_path, len(lines), "File should end with newline")
    
    def lint_file(self, file_path):
        """Lint a single markdown file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            self.add_error(file_path, 1, f"Could not read file: {e}")
            return
        
        lines = content.split('\n')
        
        # Run all checks
        self.check_file_structure(content, file_path)
        self.check_spacing_issues(lines, file_path)
        self.check_list_formatting(lines, file_path)
        self.check_bold_patterns(lines, file_path)
        self.check_line_continuity(lines, file_path)
        self.check_markdown_in_divs(lines, file_path)
        self.check_specific_patterns(lines, file_path)
        self.check_indentation(lines, file_path)
        
        self.file_count += 1
    
    def print_results(self):
        """Print linting results"""
        print(f"\n📋 Comprehensive Markdown Linting Results")
        print(f"Files checked: {self.file_count}")
        print(f"Errors: {len(self.errors)}")
        print(f"Warnings: {len(self.warnings)}")
        
        if self.errors:
            print(f"\n❌ ERRORS ({len(self.errors)}):")
            for error in self.errors[:50]:  # Show first 50
                print(f"  {error}")
            if len(self.errors) > 50:
                print(f"  ... and {len(self.errors) - 50} more errors")
        
        if self.warnings:
            print(f"\n⚠️  WARNINGS ({len(self.warnings)}):")
            for warning in self.warnings[:30]:
                print(f"  {warning}")
            if len(self.warnings) > 30:
                print(f"  ... and {len(self.warnings) - 30} more warnings")
        
        if not self.errors and not self.warnings:
            print("\n✅ All files passed comprehensive linting!")
        
        return len(self.errors)

def main():
    """Main entry point"""
    import glob
    
    linter = ComprehensiveMarkdownLinter()
    
    # Get target from command line or default to docs
    target = sys.argv[1] if len(sys.argv) > 1 else 'docs'
    
    print("🔍 Running comprehensive markdown linter...")
    
    if os.path.isfile(target):
        linter.lint_file(target)
    elif os.path.isdir(target):
        md_files = glob.glob(os.path.join(target, '**/*.md'), recursive=True)
        for file_path in sorted(md_files):
            linter.lint_file(file_path)
    else:
        print(f"Error: {target} is not a valid file or directory")
        sys.exit(1)
    
    error_count = linter.print_results()
    sys.exit(1 if error_count > 0 else 0)

if __name__ == "__main__":
    main()