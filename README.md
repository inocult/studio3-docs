# Studio3 Documentation Guide

A comprehensive 50+ page MkDocs + Material guide for Studio3, explaining how the venture building platform works through belief-driven Arenas, milestone-based progress, and community validation.

## 🚀 Quick Start

1. **Run the setup script**:
   ```bash
   chmod +x setup_studio3_docs.sh
   ./setup_studio3_docs.sh
   ```

2. **Navigate to the project**:
   ```bash
   cd studio3-docs
   source venv/bin/activate
   ```

3. **Generate initial content**:
   ```bash
   python3 generate_docs.py
   ```

4. **Start the local server**:
   ```bash
   mkdocs serve
   ```

5. **View at**: http://localhost:8000

## 📚 Documentation Structure

```
studio3-docs/
├── docs/
│   ├── index.md                    # Home page
│   ├── getting-started/            # Introduction and basics
│   │   ├── what-is-studio3.md     # Core concept explanation
│   │   ├── core-concepts.md       # Belief, NFTs, Container DAOs
│   │   ├── roles.md               # Founders, Echoes, Anchors
│   │   ├── first-arena.md         # Getting started guide
│   │   └── quickstart.md          # 5-minute quick start
│   ├── arena/                      # Arena system
│   │   ├── how-arenas-work.md     # Core mechanics
│   │   ├── belief-doubt.md        # Signaling system
│   │   ├── milestones.md          # Public commitments
│   │   └── signal-mechanics.md    # Token mechanics
│   ├── lifecycle/                  # 7-phase journey
│   │   ├── overview.md            # Complete lifecycle
│   │   ├── spark.md               # Phase 1: Ideas enter
│   │   ├── forge.md               # Phase 2: Founder duels
│   │   ├── ignition.md            # Phase 3: Company forms
│   │   ├── drift.md               # Phase 4: Find PMF
│   │   ├── orbit.md               # Phase 5: Stabilize
│   │   ├── flare.md               # Phase 6: Scale
│   │   └── ascension.md           # Phase 7: Exit
│   ├── nfts/                       # NFT system
│   │   ├── spark.md               # IP remix NFT
│   │   ├── signal.md              # Journey NFT
│   │   ├── halo.md                # Sovereignty NFT
│   │   └── genesis-wallet.md      # Container DAO wallet
│   ├── founders/                   # Founder guides
│   ├── echoes/                     # Supporter guides  
│   ├── anchors/                    # Validator guides
│   ├── tokens/                     # $SIGNAL economics
│   ├── tools/                      # Platform features
│   ├── cases/                      # Case studies
│   └── resources/                  # Templates & FAQ
├── mkdocs.yml                      # MkDocs configuration
├── requirements.txt                # Python dependencies
└── generate_docs.py               # Content generator
```

## 🎯 Key Concepts Explained

### The Three NFTs
1. **Spark NFT** 🎨 - Created from remixed IP-NFTs via Flambette marketplace
2. **Signal NFT** 📡 - Tracks the venture's entire journey and milestones
3. **Halo NFT** 🛡️ - Soulbound sovereignty token unlocked at exit

### Container DAO Model
- Lightweight governance structure that grows with the venture
- Houses all NFTs in a Genesis Wallet
- Enables community participation through $SIGNAL
- Clear path to full sovereignty at Ascension

### Belief vs Doubt
- **NOT betting or securities** - it's gamified conviction signaling
- Belief = confidence in execution ability
- Doubt = constructive skepticism that helps ventures improve
- Accurate signals earn $SIGNAL rewards

### Technology Readiness Levels (TRL)
- Phases map to TRL progression (1-9)
- Spark/Forge: TRL 1-3 (Concept)
- Ignition/Drift: TRL 3-5 (Prototype)
- Orbit/Flare: TRL 5-7 (Production)
- Ascension: TRL 7-9 (Deployment)

## 📝 Content Generation

### Generate All Base Content
```bash
python3 generate_docs.py
```

### Expand to 50+ Pages
```bash
# Run the expansion script
./expand_content.sh

# Or manually expand sections:
python3 -c "from content_expander import expand_all; expand_all()"
```

### Add Specific Sections
```bash
# Add more lifecycle details
python3 add_content.py --section lifecycle --depth detailed

# Add case studies
python3 add_content.py --section cases --real-examples

# Add technical deep dives
python3 add_content.py --section technical --topics "container-dao,signal-mechanics,nft-architecture"
```

## 🛠️ Customization

### Update Branding
1. Add logo: `docs/assets/logo.svg`
2. Update colors in `docs/stylesheets/extra.css`
3. Modify theme in `mkdocs.yml`

### Add Custom Pages
```bash
# Create new section
mkdir docs/new-section
echo "# New Section" > docs/new-section/index.md

# Update navigation in mkdocs.yml
```

### Enable Features
- Analytics: Add Google Analytics ID in `mkdocs.yml`
- Comments: Enable Disqus or similar
- Search: Already enabled with MkDocs Material
- PDF Export: `pip install mkdocs-pdf-export-plugin`

## 🚀 Deployment

### Build for Production
```bash
mkdocs build
# Output in site/ directory
```

### Deploy to GitHub Pages
```bash
mkdocs gh-deploy
```

### Deploy to Netlify
```bash
# Create netlify.toml
[build]
  command = "mkdocs build"
  publish = "site"

# Push to Git and connect to Netlify
```

## 📊 Documentation Features

### Interactive Elements
- **Signal Orb**: Animated belief visualization
- **Phase Progress**: TRL progression tracker
- **Arena Cards**: Hover effects and animations
- **Token Displays**: Formatted $SIGNAL amounts

### Navigation
- Sticky navigation tabs
- Search with highlighting
- Table of contents integration
- Breadcrumb trails

### Content Types
- Step-by-step guides
- Conceptual explanations
- Reference documentation
- Interactive examples
- Case studies
- Templates and tools

## 🔄 Continuous Improvement

### Add More Content
```bash
# Check which sections need expansion
python3 check_coverage.py

# Generate specific content
python3 generate_content.py --topic "advanced-signal-strategies"
```

### Update Existing Pages
```bash
# Refresh phase documentation with latest mechanics
python3 update_phases.py

# Add new examples
python3 add_examples.py --section arena
```

### Community Contributions
1. Fork the repository
2. Create feature branch
3. Add/update content
4. Submit pull request

## 📚 Full Content List (50+ Pages)

### Getting Started (5 pages)
- What is Studio3
- Core Concepts  
- Understanding Roles
- Your First Arena
- Quick Start Guide

### Arena System (8 pages)
- How Arenas Work
- Arena Types
- Milestone System
- Belief & Doubt Mechanics
- Signal Mechanics
- Staking Strategy
- Arena Calendar
- Advanced Tactics

### Company Lifecycle (14 pages)
- Lifecycle Overview
- Phase 1: Spark (2 pages)
- Phase 2: Forge (2 pages)
- Phase 3: Ignition (2 pages)
- Phase 4: Drift (2 pages)
- Phase 5: Orbit (2 pages)
- Phase 6: Flare (2 pages)
- Phase 7: Ascension (2 pages)
- TRL Progression Guide

### NFT System (6 pages)
- NFT Overview
- Spark NFT Deep Dive
- Signal NFT Mechanics
- Halo NFT & Sovereignty
- Genesis Wallet Guide
- IP Remixing via Flambette

### Role Guides (15 pages)
- **Founders** (5 pages): Duels, MVPs, Milestones, Container DAOs, Exit
- **Echoes** (5 pages): XP, Signals, Strategy, Community, Advanced
- **Anchors** (5 pages): Validation, Mentorship, Earning, Influence, Best Practices

### Token Economics (4 pages)
- $SIGNAL Token Overview
- Token Mechanics
- Rewards System
- Belief Economy Design

### Tools & Platform (4 pages)
- Dashboard Overview
- Arena Interface
- Signal Orb
- Analytics & Tracking

### Case Studies (3 pages)
- Successful Ventures
- Learning from Pivots
- Community Highlights

### Resources (4 pages)
- Templates Library
- Comprehensive FAQ
- Glossary
- Support & Help

**Total: 55+ pages of comprehensive documentation**

## 🤝 Support

- **Discord**: [studio3.gg/discord](https://discord.gg/studio3)
- **Forum**: [forum.studio3.xyz](https://forum.studio3.xyz)
- **Email**: docs@studio3.xyz
- **GitHub**: [github.com/studio3/docs](https://github.com/studio3/docs)

## 📄 License

This documentation is released under the MIT License. Feel free to adapt for your own projects.

---

Built with ❤️ for the Studio3 community. May your signals be accurate and your ventures successful! 🚀
