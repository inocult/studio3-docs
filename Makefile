.PHONY: lint lint-strict lint-fix build build-strict serve clean install validate help format format-check pdfs

# Default target
help:
	@echo "Studio3 Documentation Commands:"
	@echo "  lint        - Run custom markdown linter"
	@echo "  lint-strict - Run MkDocs strict build validation"
	@echo "  validate    - Run both linting methods"
	@echo "  lint-fix    - Fix common markdown issues"
	@echo "  format      - Format markdown files with Prettier"
	@echo "  format-check- Check markdown formatting without changes"
	@echo "  build       - Build the documentation with PDFs"
	@echo "  build-strict- Build with strict validation"
	@echo "  pdfs        - Generate PDF guides"
	@echo "  serve       - Serve documentation locally"
	@echo "  clean       - Clean build artifacts"
	@echo "  install     - Install dependencies"

# Custom markdown linter
lint:
	@echo "🔍 Running custom markdown linter..."
	@bash -c "source venv/bin/activate && python3 lint_markdown_strict.py docs"

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
	@echo "Note: Automated fixing not available. Please fix issues manually."

# Generate PDF guides
pdfs:
	@echo "📚 Generating PDF guides..."
	@bash -c "source venv/bin/activate && python3 generate_professional_pdfs.py"

# Build documentation
build: pdfs
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
	@rm -f docs/pdf/*.pdf

# Format markdown files with Prettier
format:
	@echo "💅 Formatting markdown files with Prettier..."
	@npm install --silent
	@npm run format

# Check markdown formatting without changes
format-check:
	@echo "🔍 Checking markdown formatting..."
	@npm install --silent
	@npm run lint:prettier

# Install dependencies
install:
	@echo "📦 Installing Python dependencies..."
	@python3 -m venv venv || true
	@bash -c "source venv/bin/activate && pip install -r requirements.txt"
	@echo "📦 Installing Node dependencies..."
	@npm install