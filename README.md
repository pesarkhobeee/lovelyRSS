# 🌟 lovelyRSS - Your Personal, Shareable RSS Reader

![lovelyRSS](https://img.shields.io/badge/lovely-RSS-ff6b6b)
[![GitHub Pages](https://img.shields.io/badge/Deploy-GitHub%20Pages-blue)](https://pages.github.com/)
[![MIT License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**lovelyRSS** turns a GitHub repository into your own personal RSS reader, making it simple to follow your favorite websites and blogs. Best of all, it creates a beautiful, static website that you can easily share with friends, allowing them to see what you're reading and discover new content in a decentralized way.

🔗 **Live Demo**: [pesarkhobeee.github.io/lovelyRSS](https://pesarkhobeee.github.io/lovelyRSS)

## Why lovelyRSS?

In a world of centralized social media, RSS is a powerful tool for taking control of your own content consumption. `lovelyRSS` builds on this by making it easy to not only follow your own feeds, but to share your reading list with others. 

- **Follow your curiosity:** Have you ever wondered what your friends and colleagues are reading? `lovelyRSS` makes it easy to find out.
- **Share your knowledge:** By sharing your own feed, you can help others discover interesting new voices on the web.
- **Simple and open:** No complex setup, no algorithms, just a simple, beautiful, and open way to read and share.

## ✨ Features

- 🔄 **Automated Updates**: Automatically checks for new posts on a schedule you set.
- 📱 **Beautiful & Simple Interface**: A clean, modern design that's easy to read on any device.
- 🚀 **Zero Maintenance**: Runs for free on GitHub Actions.
- 🎨 **Fully Customizable**: Easily change the look and feel with your own CSS.
- 📖 **Open by Design**: Your reading list is transparent and easy for others to explore.

## 🚀 Quick Start

### 1. Use This Template

Click the **"Use this template"** button to create your own copy of this repository.

### 2. Add Your Favorite Feeds

Create a file named `feeds.opml` and add the RSS feeds you want to follow. You can use `rss.opml.template` as a starting point.

```xml
<outline text="A Cool Blog" 
         title="A Cool Blog" 
         type="rss" 
         xmlUrl="https://coolblog.com/feed.xml" />
```

### 3. Enable GitHub Pages

1.  Go to your repository **Settings**.
2.  Navigate to the **"Pages"** section.
3.  Set the source to **"GitHub Actions"** and save.

### 4. Enable Actions

1.  Go to the **"Actions"** tab.
2.  Click **"I understand my workflows, go ahead and enable them."**

That's it! Your personal RSS reader will be built and deployed automatically. You can find it at `https://your-username.github.io/your-repo-name/`.

## 🛠️ Local Development

For local development, you can use the provided `Makefile` for common tasks.

- `make install`: Install all necessary dependencies.
- `make build`: Build the static site.
- `make test`: Run the test suite.
- `make clean`: Remove all generated files.

### Manual Setup

If you prefer not to use `make`, you can also set up the project manually:

1.  **Install dependencies:**
    ```bash
    uv sync --dev
    ```
2.  **Run the script:**
    ```bash
    uv run python scripts/fetch_feeds.py
    ```

## 🎨 Customization

### Personalize Your Reader

Create a `config.json` file (you can copy `config.json.template`) to change your site's title, description, and how often it updates.

### Change the Look and Feel

Create a `static/custom.css` file to add your own styles and completely change the appearance of your reader.

### Format Your Feeds File

If your `feeds.opml` file gets messy, you can automatically format it by running the "Format OPML File" workflow in the Actions tab of your repository.

## 🤝 The Spirit of Sharing

`lovelyRSS` is more than just a tool; it's an invitation to a more open and decentralized way of sharing information. By sharing your reading list, you are helping to build a more connected and curious web. 

### How to Follow a Friend

You don't have to subscribe to every feed your friend follows. Instead, you can subscribe to their `latest_rss.xml` feed. This single feed contains the latest posts from all of their subscriptions, making it easy to see what they're reading without overwhelming your own reader.

If you create your own `lovelyRSS` reader, consider sharing it with your friends and adding it to our list of community examples by opening a pull request!

## 🌟 Community Examples

-   [your-username.github.io/rss](https://your-username.github.io/rss) - Your personal reader could be here!
-   Add your reader by opening a PR!

---

**Happy Reading! 📖✨**