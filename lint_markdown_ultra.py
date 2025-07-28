#!/usr/bin/env python3
"""
Ultra-comprehensive markdown linter that catches ALL formatting issues
Based on analysis of actual rendering problems in Studio3 docs
"""

import os
import re
import sys
from pathlib import Path

class UltraMarkdownLinter:
    def __init__(self):
        self.errors = []
        self.warnings = []
        self.file_count = 0
        
    def check_spacing_issues(self, lines):
        """Check for spacing issues around punctuation and formatting"""
        errors = []
        
        for i, line in enumerate(lines):
            # Space before colon after bold
            if re.search(r'\*\*[^*]+\*\*\s+:', line):
                errors.append((i + 1, "Space between bold text and colon", line))
            
            # Missing space after colon (excluding URLs, times, emoji, and bold text ending with colon)
            if re.search(r':[^\s\n\/]', line):
                if not re.search(r'https?:|mailto:|file:|ftp:|[0-9]{1,2}:[0-9]{2}|:\w+:|::|\):|\]:|\}:|^\*\*[^*]+:\*\*$|\*\*[^*]+:\*\*\s', line):
                    errors.append((i + 1, "Missing space after colon", line))
            
            # Multiple spaces (not at line start)
            if re.search(r'[^\s]\s{2,}[^\s]', line) and not re.search(r'```|^\s*\|', line):
                errors.append((i + 1, "Multiple consecutive spaces", line))
            
            # Space before punctuation (except in code blocks)
            if re.search(r'\w\s+[,;.!?]', line) and '```' not in line:
                errors.append((i + 1, "Space before punctuation", line))
                
        return errors
    
    def check_line_issues(self, lines):
        """Check for various line-level formatting issues"""
        errors = []
        prev_line = ""
        in_arena_card = False
        in_code_block = False
        in_table = False
        
        for i, line in enumerate(lines):
            # Track state
            if '```' in line:
                in_code_block = not in_code_block
            if line.strip().startswith('|'):
                in_table = True
            elif not line.strip():
                in_table = False
                
            # Skip checks in code blocks
            if in_code_block:
                prev_line = line
                continue
            
            # Check for div blocks
            if '<div class="arena-card"' in line:
                in_arena_card = True
                if 'markdown="1"' not in line:
                    errors.append((i + 1, "arena-card div missing markdown='1' attribute", line))
            elif '<div class="grid' in line and 'markdown="1"' not in line:
                errors.append((i + 1, "grid div missing markdown='1' attribute", line))
            elif '</div>' in line and in_arena_card:
                in_arena_card = False
            
            # Headers without blank line before (unless first line or after another header)
            if line.strip().startswith('#') and prev_line.strip() and not prev_line.strip().startswith('#'):
                errors.append((i + 1, "Header should have blank line before it", line))
            
            # Tables without blank line before
            if line.strip().startswith('|') and not in_table and prev_line.strip() and not prev_line.strip().startswith('|'):
                errors.append((i + 1, "Table should have blank line before it", line))
            
            # HTML headers in divs
            if in_arena_card and re.match(r'^<h[1-6]>', line):
                if not re.match(r'^<h[1-6]>.*</h[1-6]>\s*$', line):
                    errors.append((i + 1, "Broken HTML header tag", line))
            
            # Multiple dashes at line start (not in lists or tables)
            if re.match(r'^--+\s+\w', line) and not in_table:
                errors.append((i + 1, "Multiple dashes should be single dash for list", line))
                
            # Check for orphaned formatting
            if re.match(r'^\*\*$', line.strip()) or re.match(r'^\*\*\s*$', line.strip()):
                errors.append((i + 1, "Orphaned bold markers", line))
                
            prev_line = line
            
        return errors
    
    def check_bold_patterns(self, content):
        """Check for bold pattern issues"""
        errors = []
        lines = content.split('\n')
        
        for i, line in enumerate(lines):
            # Count bold markers
            bold_count = line.count('**')
            if bold_count % 2 != 0:
                errors.append((i + 1, "Unclosed bold marker", line))
            
            # Space inside bold markers
            if re.search(r'\*\*\s+\w', line) or re.search(r'\w\s+\*\*', line):
                errors.append((i + 1, "Space inside bold markers", line))
            
            # Pattern: **text**text** (missing space between bold sections)
            if re.search(r'\*\*[^*]+\*\*[^\s*:,;.!?)\]}>][^*]*\*\*', line):
                errors.append((i + 1, "Missing space between bold sections", line))
            
            # Pattern: **Something: without closing
            if re.match(r'^[-*\s]*\*\*[^*]+:(?!\*)', line):
                if '**' not in line[line.index('**')+2:]:
                    errors.append((i + 1, "Unclosed bold with colon", line))
            
            # Pattern: text** Must or ** Must (broken bold at line boundaries)  
            if re.search(r'[^\*]\*\*\s+[A-Z]', line) and line.count('**') == 1:
                errors.append((i + 1, "Broken bold marker at line boundary", line))
                
        return errors
    
    def check_list_formatting(self, lines):
        """Check for list formatting issues"""
        errors = []
        in_list = False
        list_stack = []  # Track nested list levels
        prev_indent = -1
        
        for i, line in enumerate(lines):
            stripped = line.strip()
            current_indent = len(line) - len(line.lstrip())
            
            # Check if line is a list item
            is_list_item = re.match(r'^[-*]\s+', stripped) or re.match(r'^\d+\.\s+', stripped)
            
            if is_list_item:
                # List without blank line before (at indent 0)
                if not in_list and i > 0 and lines[i-1].strip() and current_indent == 0:
                    errors.append((i + 1, "List should have blank line before it", line))
                
                # Missing space after marker
                if re.match(r'^[-*](?!\s)', stripped) or re.match(r'^\d+\.(?!\s)', stripped):
                    errors.append((i + 1, "List marker needs space after it", line))
                
                # Double markers
                if re.match(r'^[-*]\s*[-*]\s+', stripped):
                    errors.append((i + 1, "Double list markers", line))
                
                # Broken bold in list
                if re.match(r'^[-*]\s+\*\*\s+', stripped):
                    errors.append((i + 1, "Space after opening bold in list", line))
                
                # Track list state
                in_list = True
                
                # Check indentation consistency
                if list_stack and current_indent not in [0, 2, 4, 6, 8]:
                    errors.append((i + 1, f"Non-standard list indentation: {current_indent} spaces", line))
                    
            elif stripped and in_list:
                # Check if we've left the list
                if current_indent == 0 and not re.match(r'^\s{2,}', line):
                    in_list = False
                    list_stack = []
                elif current_indent > 0 and current_indent % 2 != 0:
                    errors.append((i + 1, f"Odd indentation in list continuation: {current_indent} spaces", line))
                    
            # Check for orphaned indented items
            if re.match(r'^\s{2,}[-*]\s+', line) and not in_list:
                errors.append((i + 1, "Indented list item without parent list", line))
                
            # Special patterns in lists
            if is_list_item:
                # Pattern: - **text** : content (should split)
                if re.search(r'^[-*]\s+\*\*[^*]+\*\*\s*:\s*\w', line):
                    errors.append((i + 1, "List with bold and colon should split content to next line", line))
                    
        return errors
    
    def check_complex_structures(self, lines):
        """Check for complex markdown structure issues"""
        errors = []
        code_block_count = 0
        in_code_block = False
        
        for i, line in enumerate(lines):
            # Code blocks
            if '```' in line:
                code_block_count += 1
                in_code_block = not in_code_block
                
            if in_code_block:
                continue
                
            # Broken links
            if '[' in line:
                # Check for unclosed brackets
                open_brackets = 0
                for char in line:
                    if char == '[':
                        open_brackets += 1
                    elif char == ']':
                        open_brackets -= 1
                if open_brackets > 0:
                    errors.append((i + 1, "Unclosed link bracket", line))
                    
                # Check for malformed links
                if re.search(r'\]\s+\(', line):
                    errors.append((i + 1, "Space between link text and URL", line))
                    
            # HTML comments
            if '<!--' in line:
                if '-->' not in line and not any('-->' in lines[j] for j in range(i+1, min(i+5, len(lines)))):
                    errors.append((i + 1, "Unclosed HTML comment", line))
                    
            # Malformed HTML tags
            if '<' in line and '>' in line:
                # Check for spaces in tags
                if re.search(r'<\s+\w+', line) or re.search(r'<\w+\s+>', line):
                    errors.append((i + 1, "Spaces in HTML tag", line))
                    
        # Check for unclosed code blocks at end
        if code_block_count % 2 != 0:
            errors.append((len(lines), "Unclosed code block in file", ""))
            
        return errors
    
    def check_special_patterns(self, lines):
        """Check for special Studio3 documentation patterns"""
        errors = []
        
        for i, line in enumerate(lines):
            # Lists after bold colons on same line
            if re.search(r'\*\*[^*]+\*\*:\s*[-*]\s+', line):
                errors.append((i + 1, "List after bold colon should start on new line", line))
            
            # $STUDIO instead of $SIGNAL
            if '$STUDIO' in line:
                errors.append((i + 1, "Use $SIGNAL instead of $STUDIO", line))
            
            # Broken arena-card patterns
            if 'arena-card' in line and '<div' not in line and 'class=' not in line:
                errors.append((i + 1, "arena-card mentioned outside proper div", line))
                
            # Multiple bold sections that should be headers
            if line.count('**') >= 6 and not line.strip().startswith('#'):
                errors.append((i + 1, "Multiple bold sections - consider using headers", line))
                
            # Pattern: 1. **text** (number) content - malformed
            if re.match(r'^\d+\.\s+\*\*[^*]+\*\*\s+\(\d+\)', line):
                errors.append((i + 1, "Numbered list with parenthetical - needs reformatting", line))
                
        return errors
    
    def check_table_formatting(self, lines):
        """Check table formatting issues"""
        errors = []
        in_table = False
        
        for i, line in enumerate(lines):
            if line.strip().startswith('|'):
                # First row of table
                if not in_table:
                    in_table = True
                    # Check for blank line before
                    if i > 0 and lines[i-1].strip() and not lines[i-1].strip().startswith('|'):
                        errors.append((i + 1, "Table needs blank line before it", line))
                        
                # Check table structure
                if '|' in line:
                    # Count cells
                    cells = line.split('|')
                    # Remove empty first/last if line starts/ends with |
                    if line.strip().startswith('|'):
                        cells = cells[1:]
                    if line.strip().endswith('|'):
                        cells = cells[:-1]
                        
                    # Check for malformed separator
                    if i > 0 and in_table and re.match(r'^\s*\|[\s\-:|]+\|\s*$', line):
                        # This is a separator line
                        if not all(cell.strip() in ['', '-', ':-', '-:', ':-:', '---', ':---', '---:', ':---:'] 
                                  or all(c in ' -:' for c in cell) for cell in cells):
                            errors.append((i + 1, "Malformed table separator", line))
                            
            else:
                in_table = False
                
        return errors
    
    def check_overall_structure(self, lines):
        """Check overall document structure"""
        errors = []
        
        # Missing main header
        if not lines or not lines[0].strip().startswith('# '):
            errors.append((1, "Document should start with # (h1) header", lines[0] if lines else ""))
            
        # Multiple consecutive blank lines
        blank_count = 0
        for i, line in enumerate(lines):
            if not line.strip():
                blank_count += 1
                if blank_count > 2:
                    errors.append((i + 1, "Too many consecutive blank lines", ""))
            else:
                blank_count = 0
                
        # Check header hierarchy
        prev_level = 0
        for i, line in enumerate(lines):
            if line.strip().startswith('#'):
                level = len(line.strip().split()[0])
                if prev_level > 0 and level > prev_level + 1:
                    errors.append((i + 1, f"Header level skipped (h{prev_level} to h{level})", line))
                prev_level = level
                
        return errors
    
    def check_arena_card_patterns(self, lines):
        """Check for arena-card div patterns and ensure proper formatting"""
        errors = []
        in_arena_card = False
        arena_card_start = -1
        
        for i, line in enumerate(lines):
            # Check for arena-card div start
            if '<div class="arena-card"' in line:
                in_arena_card = True
                arena_card_start = i
                
                # Check for markdown="1" attribute
                if 'markdown="1"' not in line:
                    errors.append((i + 1, "arena-card div missing markdown=\"1\" attribute", line))
            
            # Check for div end
            elif '</div>' in line and in_arena_card:
                in_arena_card = False
                arena_card_start = -1
            
            # Check patterns inside arena-card
            elif in_arena_card:
                # Check for checklists
                if re.match(r'^[-*]\s*\[\s*\]', line.strip()):
                    # This is a checkbox list item, which is good
                    pass
                
                # Check for bold headers with colons that should have content on next line
                if re.match(r'^\*\*[^*]+:\*\*\s*$', line.strip()):
                    # Bold header with colon at end of line is good
                    pass
                elif re.match(r'^\*\*[^*]+:\*\*\s+\S', line.strip()):
                    # Bold header with content on same line
                    if i + 1 < len(lines) and not lines[i + 1].strip().startswith('-'):
                        errors.append((i + 1, "Bold header with colon should have content on next line", line))
        
        # Check for unclosed arena-card
        if in_arena_card:
            errors.append((arena_card_start + 1, "Unclosed arena-card div", lines[arena_card_start] if arena_card_start >= 0 else ""))
        
        return errors
    
    def lint_file(self, filepath):
        """Lint a single markdown file"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = content.split('\n')
            
            all_errors = []
            all_warnings = []
            
            # Run all checks
            errors = self.check_spacing_issues(lines)
            all_errors.extend([(filepath, *error) for error in errors])
            
            errors = self.check_line_issues(lines) 
            all_errors.extend([(filepath, *error) for error in errors])
            
            errors = self.check_bold_patterns(content)
            all_errors.extend([(filepath, *error) for error in errors])
            
            errors = self.check_list_formatting(lines)
            all_errors.extend([(filepath, *error) for error in errors])
            
            errors = self.check_complex_structures(lines)
            all_errors.extend([(filepath, *error) for error in errors])
            
            errors = self.check_special_patterns(lines)
            all_errors.extend([(filepath, *error) for error in errors])
            
            errors = self.check_table_formatting(lines)
            all_errors.extend([(filepath, *error) for error in errors])
            
            errors = self.check_overall_structure(lines)
            all_errors.extend([(filepath, *error) for error in errors])
            
            errors = self.check_arena_card_patterns(lines)
            all_errors.extend([(filepath, *error) for error in errors])
            
            return all_errors, all_warnings
            
        except Exception as e:
            return [(filepath, 0, f"Error reading file: {str(e)}", "")], []

def main():
    """Main entry point"""
    import glob
    
    # Get all markdown files
    md_files = []
    docs_dir = 'docs'
    
    if len(sys.argv) > 1:
        # Specific file provided
        md_files = [sys.argv[1]]
    else:
        # All files in docs
        md_files = glob.glob(os.path.join(docs_dir, '**/*.md'), recursive=True)
    
    total_errors = 0
    total_warnings = 0
    file_errors = {}
    
    print("🔍 Running Ultra Markdown Linter...")
    
    linter = UltraMarkdownLinter()
    
    for filepath in sorted(md_files):
        errors, warnings = linter.lint_file(filepath)
        if errors or warnings:
            file_errors[filepath] = (errors, warnings)
            total_errors += len(errors)
            total_warnings += len(warnings)
    
    # Report results
    print(f"\n📊 Linting Complete!")
    print(f"Files checked: {len(md_files)}")
    print(f"Files with issues: {len(file_errors)}")
    print(f"Total errors: {total_errors}")
    print(f"Total warnings: {total_warnings}")
    
    if file_errors:
        print("\n❌ ERRORS BY FILE:")
        for filepath, (errors, warnings) in sorted(file_errors.items()):
            if errors:
                print(f"\n{filepath} ({len(errors)} errors):")
                for file, line, msg, content in errors[:10]:  # Show first 10
                    preview = f" -> {content.strip()[:60]}..." if content.strip() else ""
                    print(f"  Line {line}: {msg}{preview}")
                if len(errors) > 10:
                    print(f"  ... and {len(errors) - 10} more errors")
    
    if total_errors == 0:
        print("\n✅ No errors found!")
        return 0
    else:
        print(f"\n❌ Found {total_errors} errors that need fixing")
        return 1

if __name__ == "__main__":
    sys.exit(main())