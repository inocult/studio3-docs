#!/bin/bash
# Check GitHub Pages deployment status

echo "🔍 Checking GitHub Pages deployment status..."

# Check if the site is accessible
if curl -s -o /dev/null -w "%{http_code}" https://inocult.github.io/studio3-docs/ | grep -q "200"; then
    echo "✅ Site is live at: https://inocult.github.io/studio3-docs/"
else
    echo "⏳ Site is not yet accessible. This can take a few minutes after deployment."
    echo "📝 Make sure GitHub Pages is enabled in repository settings:"
    echo "   https://github.com/inocult/studio3-docs/settings/pages"
fi

# Show last deployment commit
echo ""
echo "📦 Last deployment:"
git log gh-pages -1 --pretty=format:"Commit: %h%nDate: %ad%nMessage: %s" --date=relative