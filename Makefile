.PHONY: lint lint-strict lint-fix build build-strict serve clean install validate help

# Default target
help:
	@echo "Studio3 Documentation Commands:"
	@echo "  lint        - Run custom markdown linter"
	@echo "  lint-strict - Run MkDocs strict build validation"
	@echo "  validate    - Run both linting methods"
	@echo "  lint-fix    - Fix common markdown issues"
	@echo "  build       - Build the documentation"
	@echo "  build-strict- Build with strict validation"
	@echo "  serve       - Serve documentation locally"
	@echo "  clean       - Clean build artifacts"
	@echo "  install     - Install dependencies"

# Custom markdown linter
lint:
	@echo "🔍 Running custom markdown linter..."
	@bash -c "source venv/bin/activate && python3 lint_markdown.py docs"

# MkDocs strict validation
lint-strict:
	@echo "🔍 Running MkDocs strict validation..."
	@bash -c "source venv/bin/activate && mkdocs build --strict --quiet"

# Run both validation methods
validate: lint-strict lint
	@echo "✅ All validation checks completed"

# Fix common markdown issues
lint-fix:
	@echo "🔧 Fixing markdown issues..."
	@python3 fix_markdown_issues.py

# Build documentation
build:
	@echo "🏗️ Building documentation..."
	@bash -c "source venv/bin/activate && mkdocs build"

# Build with strict validation
build-strict:
	@echo "🏗️ Building documentation with strict validation..."
	@bash -c "source venv/bin/activate && mkdocs build --strict"

# Serve documentation locally
serve:
	@echo "🚀 Starting local server..."
	@bash -c "source venv/bin/activate && mkdocs serve"

# Clean build artifacts
clean:
	@echo "🧹 Cleaning build artifacts..."
	@rm -rf site/
	@rm -f lint_output.txt

# Install dependencies
install:
	@echo "📦 Installing dependencies..."
	@python3 -m venv venv || true
	@source venv/bin/activate && pip install mkdocs mkdocs-material pyyaml