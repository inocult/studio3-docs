# Studio3 Documentation Linting Guide

This document explains the comprehensive markdown linting system for Studio3 documentation.

## Overview

We use a two-tier validation approach:

1. **MkDocs Built-in Strict Mode** - Catches structural issues
2. **Custom Markdown Linter** - Catches formatting and style issues

## Quick Commands

```bash
# Run all validations
make validate

# Run individual validations
make lint-strict    # MkDocs validation
make lint          # Custom linter

# Build documentation
make build         # Regular build
make build-strict  # Build with validation

# Development
make serve         # Local development server
make install       # Set up environment
```

## MkDocs Built-in Validation

MkDocs `--strict` mode catches:

- **Missing files** referenced in navigation
- **Broken internal links** between pages
- **Invalid YAML** in frontmatter or config
- **Plugin errors** and configuration issues
- **Template rendering** problems

### Usage

```bash
# Command line
mkdocs build --strict

# Via Makefile
make lint-strict
```

### Configuration

The validation behavior is controlled in `mkdocs.yml`:

```yaml
validation:
  nav:
    omitted_files: warn     # Files not in navigation
    not_found: warn         # Missing referenced files  
    absolute_links: warn    # Absolute URLs in nav
  links:
    not_found: warn         # Broken internal links
    absolute_links: warn    # External links
    unrecognized_links: warn # Invalid link formats
    anchors: warn           # Missing anchor targets
```

## Custom Markdown Linter

Our custom linter (`lint_markdown.py`) catches Studio3-specific issues:

### Issues Detected

1. **Bold Formatting Problems**
   - Incomplete patterns: `**text*` → `**text**`
   - Mixed formatting: `*text**` → `**text**`

2. **List Formatting Issues**
   - Broken numbered lists: `**1. item` → `1. **item**`
   - Orphaned asterisks in lists
   - Mixed bullet/numbered patterns

3. **Arena Card Issues**
   - Missing `markdown="1"` attribute
   - Potential rendering problems in divs

4. **Studio3-Specific Rules**
   - Use `$SIGNAL` not `$STUDIO`
   - Proper emoji and formatting conventions

5. **General Quality**
   - Trailing whitespace
   - Windows line endings
   - Invalid YAML frontmatter

### Usage

```bash
# Command line
python3 lint_markdown.py docs

# Via Makefile  
make lint
```

### Sample Output

```
📋 Markdown Linting Results
Files checked: 83
Errors: 15
Warnings: 42

❌ ERRORS (15):
  docs/page.md:42: ERROR: Incomplete bold formatting: **text*
  docs/page.md:55: ERROR: Use $SIGNAL instead of $STUDIO

⚠️  WARNINGS (42):
  docs/page.md:12: WARNING: Trailing whitespace
  docs/page.md:34: WARNING: Arena card missing markdown="1" attribute
```

## Automated Validation

### GitHub Actions

Documentation is automatically validated on:
- Push to any `.md` file in `docs/`  
- Pull requests modifying documentation
- Changes to `mkdocs.yml` or linting scripts

The workflow:
1. Sets up Python and virtual environment
2. Installs MkDocs and all plugins
3. Runs `mkdocs build --strict` 
4. Runs custom linter
5. Fails if critical errors found
6. Uploads build artifacts

### Pre-commit Hooks

Install pre-commit hooks to validate before commits:

```bash
pip install pre-commit
pre-commit install
```

This will run:
- Markdown linting
- Trailing whitespace removal  
- YAML validation
- Line ending fixes

## Integration with Development

### Package.json Scripts

```json
{
  "scripts": {
    "lint": "python3 lint_markdown.py docs",
    "build": "mkdocs build",
    "serve": "mkdocs serve"
  }
}
```

### VSCode Integration

Add to `.vscode/tasks.json`:

```json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "Validate Documentation",
      "type": "shell", 
      "command": "make validate",
      "group": "test"
    }
  ]
}
```

## Best Practices

### Writing Guidelines

1. **Always use proper bold formatting**
   ```markdown
   ✅ **Correct bold text**
   ❌ **Incorrect bold text*
   ```

2. **Format numbered lists properly**
   ```markdown
   ✅ 1. **Item one** - description
   ❌ **1. **Item one** - description
   ```

3. **Use arena-card divs correctly**
   ```markdown
   ✅ <div class="arena-card" markdown="1">
   ❌ <div class="arena-card">
   ```

4. **Follow Studio3 conventions**
   ```markdown
   ✅ $SIGNAL tokens
   ❌ $STUDIO tokens
   ```

### Development Workflow

1. **Before writing**: Run `make serve` for live preview
2. **While writing**: Check formatting as you go
3. **Before committing**: Run `make validate`
4. **In CI/CD**: Automatic validation on push

### Fixing Issues

Most issues can be auto-fixed:

```bash
# Fix common formatting problems
make lint-fix

# Manual fixes for complex issues
# Edit files based on linter output
make lint        # Check remaining issues
make validate    # Full validation
```

## Extending the Linter

### Adding New Rules

Edit `lint_markdown.py` and add new check functions:

```python
def check_new_rule(self, content, file_path):
    """Check for new rule violations"""
    lines = content.split('\n')
    for i, line in enumerate(lines, 1):
        if 'pattern' in line:
            self.add_error(file_path, i, f"Rule violation: {line}")
```

### Configuration

The linter can be configured by modifying the class variables:

```python
class MarkdownLinter:
    def __init__(self):
        self.strict_mode = True      # Fail on warnings
        self.max_errors = 100        # Limit error output
        self.ignored_files = []      # Skip certain files
```

## Troubleshooting

### Common Issues

1. **"source: command not found"**
   - Make sure you're using bash: `bash -c "source venv/bin/activate"`

2. **MkDocs plugins not found**
   - Install all dependencies: `make install`

3. **Too many linter errors**
   - Fix core issues first: broken bold formatting
   - Use `make lint-fix` for automated fixes

4. **False positives**
   - Update linter rules in `lint_markdown.py`
   - Add exceptions for specific patterns

### Performance

For large documentation sets:

- Linter processes ~80 files in <5 seconds
- MkDocs builds in ~10 seconds  
- Total validation time: ~15 seconds

## Summary

This linting system ensures:

- **Consistent formatting** across all documentation
- **Early detection** of rendering issues
- **Automated validation** in CI/CD
- **Developer-friendly** tools and commands
- **Studio3-specific** quality standards

Run `make validate` before any commit to maintain documentation quality!