import os

def get_stylesheet():
    return """
    /* Studio3 PDF Theme */
    @page {
        size: A4;
        margin: 2cm 1.5cm;
        @bottom-center {
            content: "Studio3 Documentation - Page " counter(page) " of " counter(pages);
            font-size: 10px;
            color: #666;
        }
    }
    
    body {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        font-size: 11pt;
        line-height: 1.6;
        color: #333;
    }
    
    /* Headers */
    h1, h2, h3, h4, h5, h6 {
        color: #2B4C8C;
        page-break-after: avoid;
        margin-top: 1.5em;
        margin-bottom: 0.5em;
    }
    
    h1 {
        font-size: 24pt;
        border-bottom: 3px solid #E91E63;
        padding-bottom: 0.5em;
    }
    
    h2 {
        font-size: 18pt;
        border-bottom: 2px solid #E91E63;
        padding-bottom: 0.3em;
    }
    
    h3 {
        font-size: 14pt;
    }
    
    /* Links */
    a {
        color: #E91E63;
        text-decoration: none;
    }
    
    /* Code blocks */
    pre {
        background-color: #f8f8f8;
        border: 1px solid #ddd;
        border-radius: 4px;
        padding: 10px;
        font-size: 9pt;
        overflow-x: auto;
        page-break-inside: avoid;
    }
    
    code {
        background-color: rgba(233, 30, 99, 0.1);
        color: #E91E63;
        padding: 2px 4px;
        border-radius: 3px;
        font-size: 9pt;
    }
    
    /* Tables */
    table {
        width: 100%;
        border-collapse: collapse;
        margin: 1em 0;
        page-break-inside: avoid;
    }
    
    th {
        background-color: #2B4C8C;
        color: white;
        padding: 8px;
        text-align: left;
        font-weight: 600;
    }
    
    td {
        border: 1px solid #ddd;
        padding: 8px;
    }
    
    tr:nth-child(even) {
        background-color: rgba(43, 76, 140, 0.05);
    }
    
    /* Admonitions */
    .admonition {
        border-left: 4px solid #E91E63;
        padding: 10px 15px;
        margin: 1em 0;
        page-break-inside: avoid;
        background-color: rgba(233, 30, 99, 0.05);
    }
    
    .admonition-title {
        font-weight: 600;
        color: #2B4C8C;
        margin-bottom: 0.5em;
    }
    
    /* Arena cards */
    .arena-card {
        border: 2px solid #E91E63;
        border-radius: 8px;
        padding: 15px;
        margin: 1em 0;
        page-break-inside: avoid;
        background-color: #f9f9f9;
    }
    
    .arena-card h3, .arena-card h4 {
        color: #2B4C8C;
        margin-top: 0;
    }
    
    /* Phase indicators */
    .phase-indicator {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 15px;
        font-size: 10pt;
        font-weight: 600;
        color: white;
        background-color: #666;
        margin: 2px;
    }
    
    /* Grid layout for PDF */
    .grid {
        display: block;
    }
    
    .grid > * {
        margin-bottom: 1em;
    }
    
    /* Page breaks */
    h1 {
        page-break-before: always;
    }
    
    h1:first-child {
        page-break-before: avoid;
    }
    
    /* Hide interactive elements */
    .md-button,
    .signal-orb,
    .loading-spinner,
    button {
        display: none !important;
    }
    
    /* Images */
    img {
        max-width: 100%;
        height: auto;
        display: block;
        margin: 1em auto;
    }
    
    /* Lists */
    ul, ol {
        margin-left: 1.5em;
        margin-bottom: 1em;
    }
    
    li {
        margin-bottom: 0.3em;
    }
    
    /* Blockquotes */
    blockquote {
        border-left: 4px solid #2B4C8C;
        padding-left: 1em;
        margin: 1em 0;
        font-style: italic;
        color: #666;
    }
    """

def modify_html(html: str, href: str) -> str:
    """Modify HTML before PDF conversion"""
    # Add title page content
    title_page = '''
    <div style="text-align: center; margin-top: 100px;">
        <h1 style="font-size: 36pt; color: #2B4C8C; border: none;">Studio3 Documentation</h1>
        <p style="font-size: 18pt; color: #666; margin-top: 20px;">Where Belief Becomes Momentum</p>
        <p style="font-size: 14pt; color: #E91E63; margin-top: 40px;">The Complete Guide to Building Ventures Through Belief-Driven Arenas</p>
    </div>
    <div style="page-break-after: always;"></div>
    '''
    
    # Insert title page after body tag
    html = html.replace('<body>', f'<body>{title_page}')
    
    return html