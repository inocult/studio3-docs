#!/bin/bash
# Deploy Studio3 documentation to GitHub Pages

echo "🚀 Deploying Studio3 documentation to GitHub Pages..."

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Build the documentation
echo "📚 Building documentation..."
mkdocs build --clean

# Deploy to GitHub Pages
echo "🌐 Deploying to GitHub Pages..."
mkdocs gh-deploy --force --clean --message "Deploy documentation to GitHub Pages"

echo "✅ Deployment complete!"
echo "🔗 View at: https://inocult.github.io/studio3-docs/"