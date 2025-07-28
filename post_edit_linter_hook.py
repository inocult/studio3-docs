#!/usr/bin/env python3
"""
Post-edit hook for claude-code to run linter and fix errors automatically.
This hook runs after any file edit to check and fix markdown formatting issues.
"""

import os
import sys
import json
import subprocess
import re

def run_linter_on_file(file_path):
    """Run the markdown linter on a specific file and return errors."""
    if not file_path.endswith('.md'):
        return []
    
    try:
        # Run the linter on just this file
        result = subprocess.run(
            [sys.executable, 'lint_markdown_ultra.py', file_path],
            capture_output=True,
            text=True,
            cwd=os.path.dirname(os.path.abspath(__file__))
        )
        
        # Parse the output to get errors
        errors = []
        lines = result.stdout.split('\n')
        
        # Find the file's error section
        in_file_errors = False
        for line in lines:
            if file_path in line and 'errors)' in line:
                in_file_errors = True
                continue
            elif in_file_errors and line.strip() == '':
                break
            elif in_file_errors and 'Line' in line:
                # Parse error: "  Line 123: Error message -> content..."
                match = re.match(r'\s*Line (\d+): (.+?) -> (.+)$', line)
                if match:
                    line_num = int(match.group(1))
                    error_type = match.group(2)
                    content = match.group(3)
                    errors.append({
                        'line': line_num,
                        'error': error_type,
                        'content': content
                    })
        
        return errors
    except Exception as e:
        print(f"Error running linter: {e}", file=sys.stderr)
        return []

def fix_common_errors(file_path, errors):
    """Automatically fix common formatting errors."""
    if not errors:
        return False
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        modified = False
        
        # Sort errors by line number in reverse order to avoid offset issues
        errors.sort(key=lambda x: x['line'], reverse=True)
        
        for error in errors:
            line_idx = error['line'] - 1
            if line_idx >= len(lines):
                continue
                
            line = lines[line_idx]
            error_type = error['error']
            
            # Fix space after opening bold marker: **text -> **text
            if error_type == "Space after opening bold marker":
                fixed_line = re.sub(r'\*\*\s+([^*])', r'**\1', line)
                if fixed_line != line:
                    lines[line_idx] = fixed_line
                    modified = True
            
            # Fix space before closing bold marker: text ** -> text**
            elif error_type == "Space before closing bold marker":
                fixed_line = re.sub(r'([^*])\s+\*\*', r'\1**', line)
                if fixed_line != line:
                    lines[line_idx] = fixed_line
                    modified = True
            
            # Fix missing space after colon (but not in URLs)
            elif error_type == "Missing space after colon":
                fixed_line = re.sub(r'(?<!http)(?<!https):(?![/\d])(?!\s)', ': ', line)
                if fixed_line != line:
                    lines[line_idx] = fixed_line
                    modified = True
            
            # Fix list after bold colon on same line
            elif error_type == "List after bold colon should start on new line":
                # Split at the list marker
                match = re.search(r'(\*\*[^*]+\*\*:)\s*([-*]\s+.*)$', line)
                if match:
                    lines[line_idx] = match.group(1) + '\n'
                    lines.insert(line_idx + 1, '\n')
                    lines.insert(line_idx + 2, match.group(2) + '\n')
                    modified = True
            
            # Fix bold header with colon needing blank line before list
            elif error_type == "Bold header with colon needs blank line before list":
                # Check if next line is a list
                if line_idx + 1 < len(lines):
                    next_line = lines[line_idx + 1].strip()
                    if re.match(r'^[-*\d]', next_line):
                        # Insert blank line after the bold header
                        lines.insert(line_idx + 1, '\n')
                        modified = True
        
        if modified:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.writelines(lines)
            return True
        
        return False
        
    except Exception as e:
        print(f"Error fixing file: {e}", file=sys.stderr)
        return False

def main():
    """Main hook function."""
    # Get the file path from the hook environment or command line
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
    else:
        # Try to get from environment variable (claude-code might set this)
        file_path = os.environ.get('EDITED_FILE_PATH', '')
    
    if not file_path or not os.path.exists(file_path):
        print("No valid file path provided", file=sys.stderr)
        return 0
    
    # Only process markdown files
    if not file_path.endswith('.md'):
        return 0
    
    print(f"🔍 Running linter on {file_path}...")
    
    # Run linter on the file
    errors = run_linter_on_file(file_path)
    
    if errors:
        print(f"Found {len(errors)} formatting issues")
        
        # Attempt to fix common errors
        if fix_common_errors(file_path, errors):
            print("✅ Fixed some formatting issues automatically")
            
            # Run linter again to check remaining issues
            remaining_errors = run_linter_on_file(file_path)
            if remaining_errors:
                print(f"⚠️  {len(remaining_errors)} issues remain that need manual fixing:")
                for error in remaining_errors[:5]:  # Show first 5
                    print(f"  Line {error['line']}: {error['error']}")
                if len(remaining_errors) > 5:
                    print(f"  ... and {len(remaining_errors) - 5} more")
        else:
            print("ℹ️  Found issues that need manual fixing:")
            for error in errors[:5]:  # Show first 5
                print(f"  Line {error['line']}: {error['error']}")
            if len(errors) > 5:
                print(f"  ... and {len(errors) - 5} more")
    else:
        print("✅ No formatting issues found")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())