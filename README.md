# Studio3 Documentation

Complete documentation for Studio3 - Where Belief Becomes Momentum.

## 🌐 Live Documentation

Visit the live documentation at: https://inocult.github.io/studio3-docs/

## 📚 Documentation Structure

The documentation is organized into 4 comprehensive guides:

1. **Overview Guide** - Complete introduction to Studio3
2. **Senders Guide** - For founders building ventures
3. **Echoes Guide** - For supporters signaling belief
4. **Anchors Guide** - For validators ensuring quality

## 🛠️ Local Development

### Prerequisites

- Python 3.8+
- pip

### Setup

1. Clone the repository:
```bash
git clone https://github.com/inocult/studio3-docs.git
cd studio3-docs
```

2. Create virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

### Running Locally

```bash
mkdocs serve
```

Visit http://localhost:8000 to see the documentation.

## 🚀 Deployment

### Automatic Deployment

The documentation automatically deploys to GitHub Pages when changes are pushed to the `main` branch.

### Manual Deployment

To manually deploy:

```bash
./deploy.sh
```

Or using mkdocs directly:

```bash
mkdocs gh-deploy
```

## 📄 PDF Generation

To generate PDF versions of the documentation:

```bash
ENABLE_PDF_EXPORT=1 mkdocs build
```

PDFs will be available in the `site/pdf/` directory.

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Built with [MkDocs](https://www.mkdocs.org/)
- Styled with [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/)
- Deployed with [GitHub Pages](https://pages.github.com/)