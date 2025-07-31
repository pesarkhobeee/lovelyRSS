# 🌟 lovelyRSS - Static RSS Hub Generator

![RSS Hub](https://img.shields.io/badge/📰_RSS_Hub-Updated_every_6h-brightgreen)
[![GitHub Pages](https://img.shields.io/badge/GitHub%20Pages-Deploy-blue)](https://pages.github.com/)
[![MIT License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**lovelyRSS** is a beautiful, static RSS hub generator that transforms any GitHub repository into your personal RSS reading hub. It encourages open sharing of reading habits and interests in a transparent, decentralized way.

🔗 **Live Demo**: [pesarkhobeee.github.io/lovelyRSS](https://pesarkhobeee.github.io/lovelyRSS)

## ✨ Features

- 🔄 **Automated Updates**: Fetches feeds every 6 hours via GitHub Actions
- 📱 **Beautiful Web Interface**: Clean, responsive design with dark/light mode
- 📊 **Multiple Output Formats**: RSS XML, JSON Feed, and HTML
- 🏷️ **Category Support**: Organize feeds by topics
- 🚀 **Zero Maintenance**: Everything runs automatically on GitHub
- 🎨 **Customizable**: Easy to modify templates and styling
- 📖 **Open Source**: Your reading habits are transparent and shareable
- 🌐 **Standards Compliant**: Follows RSS 2.0, JSON Feed, and OPML specifications

## 🚀 Quick Start

### 1. Use This Template

Click the **"Use this template"** button or [create a new repository](https://github.com/your-username/lovely-rss/generate).

### 2. Add Your RSS Feeds

Create a new file named `feeds.opml` and add your favorite RSS feeds. You can use `rss.opml.template` as a starting point.

```xml
<outline text="Your Blog" 
         title="Your Blog" 
         type="rss" 
         xmlUrl="https://yourblog.com/feed.xml"
         htmlUrl="https://yourblog.com/"
         category="Blogs"/>
```

### 3. Enable GitHub Pages

1. Go to your repository **Settings**
2. Navigate to **"Pages"** section
3. Set source to **"GitHub Actions"**
4. Save the settings

### 4. Enable Actions

1. Go to the **"Actions"** tab
2. Click **"I understand my workflows, go ahead and enable them"**
3. The workflow will run automatically

### 5. Wait for the Magic ✨

GitHub Actions will automatically:
- 📡 Fetch all your RSS feeds
- 🎨 Generate a beautiful HTML page
- 📄 Create merged RSS/JSON files
- 🚀 Deploy everything to GitHub Pages

Your RSS hub will be available at: `https://your-username.github.io/your-repo-name/`

## 📁 Repository Structure

```
lovely-rss/
├── 📝 feeds.opml                # Your RSS feed list (create this file!)
├── 📝 rss.opml.template         # An example feed list
├── 📝 config.json               # Your site configuration (create this file!)
├── 📝 config.json.template      # An example configuration file
├── 📝 static/custom.css         # Your custom styles (create this file!)
├── 🤖 latest_rss.xml            # Auto-generated: latest posts from all feeds
├── 🤖 latest_feeds.xml          # Auto-generated: feed metadata
├── 🤖 latest_posts.json         # Auto-generated: JSON feed format
├── 🤖 index.html                # Auto-generated: beautiful web interface
├── 📁 scripts/
│   ├── 🐍 fetch_feeds.py        # Main RSS processing script
│   └── 🔧 utils.py              # Utility functions
├── 📁 templates/
│   └── 🎨 index.html            # Jinja2 HTML template
├── 📁 static/
│   └── 📄 README.md             # Static assets info
├── 📁 .github/workflows/
│   └── ⚙️ update_feeds.yml      # GitHub Actions automation
├── 📦 pyproject.toml            # Python dependencies (using uv)
├── 📖 README.md                 # This file
└── 📄 plan.md                   # Original project plan
```

## 🛠️ Local Development

### Prerequisites

- Python 3.8+
- [uv](https://docs.astral.sh/uv/) (recommended) or pip

### Setup

```bash
# Clone your repository
git clone https://github.com/your-username/your-rss-hub.git
cd your-rss-hub

# Create your feed and config files
cp rss.opml.template feeds.opml
cp config.json.template config.json

# Install dependencies with uv (recommended)
uv sync

# Or with pip (create requirements.txt first)
pip install feedparser requests jinja2 beautifulsoup4 python-dateutil

# Run the script
uv run python scripts/fetch_feeds.py
```

### Testing Your OPML

Add some test feeds to `rss.opml` and run the script to see the generated files:

```bash
# Generate all files locally
uv run python scripts/fetch_feeds.py

# Open the generated HTML file
open index.html  # macOS
xdg-open index.html  # Linux
start index.html  # Windows
```

## 🎨 Customization

### Configuration

Create a `config.json` file (you can copy `config.json.template`) to customize site-wide settings:

- `site_title`: The main title of your RSS hub.
- `site_description`: A short description of your hub.
- `site_link`: A link to your project or website.
- `generator`: The name of the generator.
- `output_files`: The names of the generated files.
- `max_entries`: The maximum number of entries to include in each file type.

### HTML Template

The main template is in `templates/index.html`. You can customize:

- **Colors and themes**: Modify CSS variables in `:root`
- **Layout**: Adjust the grid systems and component layouts
- **Content sections**: Add/remove sections as needed
- **Branding**: Update titles, descriptions, and links

### Feed Processing

Customize `scripts/fetch_feeds.py` to:

- **Change update frequency**: Modify entry limits
- **Add new output formats**: Extend generation functions
- **Custom filtering**: Filter feeds by keywords or dates
- **Enhanced metadata**: Extract additional feed information

### Styling

1. **Dark/Light Mode**: Automatically handled via CSS `prefers-color-scheme`
2. **Custom CSS**: Create a `static/custom.css` file to add your own styles. This file will override the default styles.
3. **Responsive Design**: Built-in responsive breakpoints

### Categories

Organize your feeds using the `category` attribute in OPML:

```xml
<outline text="Tech News" 
         category="Technology"
         .../>
<outline text="Personal Blog" 
         category="Blogs"
         .../>
```

### GitHub Actions Schedule

Edit `.github/workflows/update_feeds.yml` to change update frequency:

```yaml
schedule:
  - cron: "0 */3 * * *"  # Every 3 hours
  - cron: "0 8 * * *"    # Once daily at 8 AM UTC
  - cron: "0 12 * * 1"   # Weekly on Monday at noon
```

## 📊 Output Formats

### RSS XML (`latest_rss.xml`)
Standard RSS 2.0 format with latest posts from all feeds.

### JSON Feed (`latest_posts.json`)
JSON Feed 1.1 format for modern applications and APIs.

### Feed List XML (`latest_feeds.xml`)
Metadata about all subscribed feeds, sorted by recent updates.

### HTML (`index.html`)
Beautiful web interface with responsive design.

## 🔧 Advanced Configuration

### Custom Domain

To use a custom domain with GitHub Pages:

1. Add a `CNAME` file to your repository root:
   ```
   your-rss-hub.example.com
   ```
2. Configure your domain's DNS with a CNAME record
3. Update GitHub Pages settings to use the custom domain

### Private Feeds

For feeds requiring authentication:

1. Use GitHub Secrets to store credentials
2. Modify `fetch_feeds.py` to handle authentication:
   ```python
   headers = {
       'Authorization': f'Bearer {os.environ["FEED_TOKEN"]}',
       'User-Agent': 'lovelyRSS/1.0'
   }
   ```
3. Update the workflow to pass secrets

### Analytics

Add privacy-friendly analytics:

1. **Plausible Analytics** (recommended):
   ```html
   <script defer data-domain="yourdomain.com" 
           src="https://plausible.io/js/script.js"></script>
   ```

2. **Simple Analytics**:
   ```html
   <script async defer src="https://scripts.simpleanalyticscdn.com/latest.js"></script>
   ```

### Performance Optimization

1. **Feed Caching**: Implement conditional requests with ETags
2. **Image Optimization**: Process and optimize feed images
3. **CDN**: Use GitHub's CDN or integrate with Cloudflare

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

- 🐛 **Report bugs** via GitHub Issues
- 💡 **Suggest features** with detailed use cases
- 🔧 **Submit pull requests** with improvements
- ⭐ **Star the repository** to show support
- 📢 **Share your RSS hub** to inspire others

### Development Guidelines

1. Follow Python PEP 8 style guidelines
2. Add type hints to new functions
3. Update documentation for new features
4. Test changes locally before submitting PRs

## 🌟 Community Examples

RSS hubs built with lovelyRSS:

- `your-username.github.io/rss` - Your personal hub
- Add your RSS hub here by opening a PR!

## 🚨 Troubleshooting

### Feeds not updating?

1. **Check Actions logs**: Go to Actions tab → latest workflow run
2. **Verify OPML**: Ensure `feeds.opml` is valid XML
3. **Test feed URLs**: Manually check if feeds are accessible
4. **Check rate limits**: Some feeds may have rate limiting

### GitHub Pages not working?

1. **Enable Pages**: Repository Settings → Pages → GitHub Actions
2. **Check workflow**: Ensure the workflow completed successfully
3. **Verify files**: Check that `index.html` was generated
4. **Repository visibility**: Ensure repo is public (or you have GitHub Pro)

### Local script failing?

1. **Install dependencies**: `uv sync` or check requirements
2. **Verify OPML**: Ensure `rss.opml` exists and is valid
3. **Check connectivity**: Test internet connection
4. **Python version**: Ensure Python 3.8+ is installed

### Common Issues

**Issue**: "Import feedparser could not be resolved"
**Solution**: Install dependencies: `uv sync` or `pip install feedparser`

**Issue**: "No feeds found in OPML file"
**Solution**: Check OPML format and ensure `xmlUrl` attributes are present

**Issue**: "GitHub Actions failing"
**Solution**: Check if repository has Actions enabled and workflow file is in the correct location

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🙏 Acknowledgments

- **RSS Community**: For keeping syndication alive and thriving
- **GitHub**: For providing free hosting and automation
- **Python Community**: For excellent libraries like feedparser and Jinja2
- **Web Standards**: RSS 2.0, JSON Feed, and OPML specifications

## 📞 Support

- **Documentation**: Check this README and inline code comments
- **Issues**: [GitHub Issues](https://github.com/your-username/lovely-rss/issues)
- **Discussions**: [GitHub Discussions](https://github.com/your-username/lovely-rss/discussions)
- **Email**: [your-email@example.com](mailto:your-email@example.com)

---

**Happy RSS reading! 📖✨**

Built with ❤️ by the RSS community. Made possible by GitHub Actions, Python, and the timeless beauty of RSS feeds.

---

*lovelyRSS - Because your reading habits deserve to be shared beautifully.*
