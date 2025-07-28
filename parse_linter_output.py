#!/usr/bin/env python3
import subprocess
import re
import sys

def parse_linter_output():
    """Run the linter and parse its output to show files sorted by error count."""
    try:
        # Run the linter
        result = subprocess.run(['python3', 'lint_markdown_ultra.py'], 
                              capture_output=True, text=True)
        
        output = result.stderr if result.stderr else result.stdout
        
        # Parse error counts from lines like: "docs/path/file.md (123 errors):"
        error_pattern = r'^(docs/[^(]+) \((\d+) errors\):$'
        
        files_with_errors = []
        
        for line in output.split('\n'):
            match = re.match(error_pattern, line)
            if match:
                file_path = match.group(1)
                error_count = int(match.group(2))
                files_with_errors.append((error_count, file_path))
        
        # Sort by error count (descending)
        files_with_errors.sort(reverse=True)
        
        # Display results
        print("📊 Files Sorted by Error Count (Highest to Lowest):")
        print("=" * 60)
        
        if not files_with_errors:
            print("No files with errors found in the linter output.")
            print("\nRaw output:")
            print(output)
            return
        
        for i, (error_count, file_path) in enumerate(files_with_errors, 1):
            print(f"{i:2d}. {error_count:3d} errors - {file_path}")
        
        print(f"\nTotal files with errors: {len(files_with_errors)}")
        print(f"Total errors across all files: {sum(count for count, _ in files_with_errors)}")
        
        # Show top 10 files for priority fixing
        if len(files_with_errors) > 10:
            print(f"\n🎯 TOP 10 PRIORITY FILES FOR FIXING:")
            print("-" * 40)
            for i, (error_count, file_path) in enumerate(files_with_errors[:10], 1):
                print(f"{i:2d}. {error_count:3d} errors - {file_path}")
        
    except Exception as e:
        print(f"Error running or parsing linter: {e}")
        sys.exit(1)

if __name__ == "__main__":
    parse_linter_output()