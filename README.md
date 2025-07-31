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

Getting started with your own personal RSS reader is as simple as 1-2-3.

### 1. Create Your Own Copy

Click the **"Use this template"** button to create your own copy of this repository.

### 2. Add Your Favorite Feeds

Create a file named `feeds.opml` and add the RSS feeds you want to follow. You can use `rss.opml.template` as a starting point.

### 3. Enable GitHub Pages & Actions

1.  Go to your repository **Settings** > **Pages** and set the source to **"GitHub Actions"**.
2.  Go to the **"Actions"** tab and click **"I understand my workflows, go ahead and enable them."**

That's it! Your personal RSS reader will be built and deployed automatically. You can find it at `https://your-username.github.io/your-repo-name/`.

## 🎨 Customization

Once you have your reader up and running, you can personalize it to make it your own.

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

We encourage you to share your reader with your friends and on your social media. Let's build a more open web together!

## 🌟 Community Examples

-   [your-username.github.io/rss](https://your-username.github.io/rss) - Your personal reader could be here!
-   Add your reader by opening a PR!

## What's Next?

Now that you have your own personal RSS reader, here are a few things you can do:

-   **Add more feeds:** Start building your collection of your favorite sites and blogs.
-   **Customize your reader:** Change the colors, fonts, and layout to make it your own.
-   **Share it with the world:** Share your reader with your friends and encourage them to create their own.

---

**Happy Reading! 📖✨**
