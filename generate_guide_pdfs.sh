#!/bin/bash
# Generate separate PDFs for each guide

echo "🚀 Generating Studio3 Guide PDFs..."

# Activate virtual environment
source venv/bin/activate

# Create PDF directory if it doesn't exist
mkdir -p site/pdf

# Generate Overview Guide PDF
echo "📚 Generating Overview Guide PDF..."
ENABLE_PDF_EXPORT=1 mkdocs build --config-file mkdocs-overview.yml

# Generate Senders Guide PDF  
echo "🏗️ Generating Senders Guide PDF..."
ENABLE_PDF_EXPORT=1 mkdocs build --config-file mkdocs-senders.yml

# Generate Echoes Guide PDF
echo "📡 Generating Echoes Guide PDF..."
ENABLE_PDF_EXPORT=1 mkdocs build --config-file mkdocs-echoes.yml

# Generate Anchors Guide PDF
echo "⚓ Generating Anchors Guide PDF..."
ENABLE_PDF_EXPORT=1 mkdocs build --config-file mkdocs-anchors.yml

# Generate complete documentation
echo "📖 Building complete documentation site..."
mkdocs build

echo "✅ All PDFs generated successfully!"
echo "📁 PDFs available in site/pdf/"