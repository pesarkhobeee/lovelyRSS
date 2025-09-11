# 🌟 lovelyRSS - Your Personal, Shareable RSS Reader

![lovelyRSS](https://img.shields.io/badge/lovely-RSS-ff6b6b)
[![GitHub Pages](https://img.shields.io/badge/Deploy-GitHub%20Pages-blue)](https://pages.github.com/)
[![MIT License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**lovelyRSS** turns a GitHub repository into your own personal RSS reader, making it simple to follow your favorite websites and blogs. Best of all, it creates a beautiful, static website that you can easily share with friends, allowing them to see what you're reading and discover new content in a decentralized way.

🔗 **Live Demo**: [pesarkhobeee.github.io/lovelyRSS](https://pesarkhobeee.github.io/lovelyRSS)

<details>
<summary><strong>Why lovelyRSS? 🤔</strong></summary>

In a world of centralized social media, RSS is a powerful tool for taking control of your own content consumption. `lovelyRSS` builds on this by making it easy to not only follow your own feeds, but to share your reading list with others. 

- **Follow your curiosity:** Have you ever wondered what your friends and colleagues are reading? `lovelyRSS` makes it easy to find out.
- **Share your knowledge:** By sharing your own feed, you can help others discover interesting new voices on the web.
- **Simple and open:** No complex setup, no algorithms, just a simple, beautiful, and open way to read and share.

</details>

<details>
<summary><strong>✨ Features</strong></summary>

- 🔄 **Automated Updates**: Automatically checks for new posts on a schedule you set.
- 📱 **Beautiful & Simple Interface**: A clean, modern design that's easy to read on any device.
- 🚀 **Zero Maintenance**: Runs for free on GitHub Actions.
- 🎨 **Fully Customizable**: Easily change the look and feel with your own CSS.
- 📖 **Open by Design**: Your reading list is transparent and easy for others to explore.

</details>

<details>
<summary><strong>🚀 Quick Start</strong></summary>

Getting started with your own personal RSS reader is as simple as 1-2-3.

### 1. Create Your Own Copy

Click the **"Fork"** button to create your own copy of this repository.

### 2. Add Your Favorite Feeds

Create a file named `feeds.opml` and add the RSS feeds you want to follow. You can use `rss.opml.template` as a starting point.

### 3. Enable GitHub Pages & Actions

1.  Go to your repository **Settings** > **Pages** and set the source to **"GitHub Actions"**.
2.  Go to the **"Actions"** tab and click **"I understand my workflows, go ahead and enable them."**

That's it! Your personal RSS reader will be built and deployed automatically. You can find it at `https://your-username.github.io/your-repo-name/`.

</details>

<details>
<summary><strong>🎨 Customization</strong></summary>

Once you have your reader up and running, you can personalize it to make it your own.

### Personalize Your Reader

Create a `config.json` file (you can copy `config.json.template`) to change your site's title, description, and how often it updates.

### Change the Look and Feel

Create a `static/custom.css` file to add your own styles and completely change the appearance of your reader.

### Format Your Feeds File

If your `feeds.opml` file gets messy, you can automatically format it by running the "Format OPML File" workflow in the Actions tab of your repository.

</details>

<details>
<summary><strong>🤝 The Spirit of Sharing</strong></summary>

`lovelyRSS` is more than just a tool; it's an invitation to a more open and decentralized way of sharing information. By sharing your reading list, you are helping to build a more connected and curious web.

### How to Follow a Friend

Instead of subscribing to every feed your friend follows, you can subscribe to their generated `latest_rss.xml` feed. This single feed contains the latest posts from all of their subscriptions, making it easy to see what they're reading without overwhelming your own reader.

We encourage you to share your reader with your friends and on your social media. Let's build a more open web together!

### Generated Files for Sharing

Your `lovelyRSS` instance produces several files that make it easy to share what you're reading:

-   **`index.html`**: The main, shareable webpage that displays your feeds and the latest posts.
-   **`latest_rss.xml`**: A merged RSS feed of the latest posts from all your subscriptions. This is perfect for friends who want to follow your reading list in their own RSS reader.
-   **`latest_posts.json`**: A JSON file containing the latest posts, ideal for developers who want to use your data in other applications.
-   **`latest_feeds.xml`**: An XML file listing all the feeds you subscribe to, sorted by the most recently updated.

These files are updated automatically and can be found at `https://your-username.github.io/your-repo-name/`.

</details>

<details>
<summary><strong>🔄 Updating Your Fork</strong></summary>

One of the goals of `lovelyRSS` is to make it easy to keep your personal reader up-to-date with the latest features. We have designed the workflow to be completely conflict-free, so you can pull in the latest changes without any risk of losing your personal configurations.

Since your `feeds.opml` and `config.json` files are not tracked by git, you can safely fetch the latest changes from the main repository without creating any merge conflicts. Your reader will simply be updated with the newest features, and your feeds will be regenerated on the next scheduled run.

To update your fork, simply run the following commands in your local repository:

```bash
git fetch upstream
git merge upstream/main
```

This will keep your reader current while preserving your unique feed list and settings.

</details>

<details>
<summary><strong>🌟 Community Examples</strong></summary>

-   [pesarkhobeeee.github.io/rss](https://pesarkhobeee.github.io/rss/)
-   [your-username.github.io/rss](https://your-username.github.io/rss) - Your personal reader could be here!
-   Add your reader by opening a PR!

</details>

<details>
<summary><strong>What's Next? 🎯</strong></summary>

Now that you have your own personal RSS reader, here are a few things you can do:

-   **Add more feeds:** Start building your collection of your favorite sites and blogs.
-   **Customize your reader:** Change the colors, fonts, and layout to make it your own.
-   **Share it with the world:** Share your reader with your friends and encourage them to create their own.

</details>

---

**Happy Reading! 📖✨**