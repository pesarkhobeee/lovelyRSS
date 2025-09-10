# Favicon Support Feature

This document describes the favicon functionality added to lovelyRSS, which automatically fetches and displays website favicons for RSS feeds.

## Overview

The favicon feature enhances the visual appeal of the RSS reader by displaying small icons next to feed names and entries, making it easier to identify different sources at a glance.

## Features

### Automatic Favicon Detection
- Automatically fetches favicons from feed websites
- Tries multiple common favicon locations (`/favicon.ico`, `/favicon.png`, `/apple-touch-icon.png`)
- Parses HTML to find `<link rel="icon">` tags for custom favicon locations
- Falls back gracefully when favicons are not found

### Special Platform Support

#### GitHub Profile Feeds
For GitHub profile feeds (e.g., `https://github.com/username.atom`), the system automatically uses the user's GitHub profile image:
- Format: `https://github.com/username.png?size=50`
- Works for both user profiles and repository feeds
- Provides a consistent 50x50 pixel size for optimal display

#### YouTube Feeds
YouTube channel feeds automatically use the YouTube favicon for consistent branding.

#### Platform-Specific Handling
- **Stack Overflow**: Uses the official Stack Overflow favicon
- **Hacker News**: Uses the Y Combinator favicon
- **BBC**: Uses BBC-specific favicon from their CDN

### Visual Integration

#### Feed Listings
Favicons appear in the feeds section:
```html
<span class="feed-title">
    <img src="favicon-url" alt="favicon" class="feed-favicon" />
    Feed Name
</span>
```

#### Entry Sources
Favicons appear next to entry sources in the latest posts:
```html
<span class="entry-source">
    <img src="favicon-url" alt="favicon" class="entry-favicon" />
    Feed Name
</span>
```

## CSS Styling

### Feed Favicons
```css
.feed-favicon {
    width: 16px;
    height: 16px;
    border-radius: 3px;
    flex-shrink: 0;
    object-fit: cover;
    background: var(--border-color);
}
```

### Entry Favicons
```css
.entry-favicon {
    width: 14px;
    height: 14px;
    border-radius: 2px;
    flex-shrink: 0;
    object-fit: cover;
    background: var(--border-color);
}
```

## Implementation Details

### Core Functions

#### `get_favicon_url(feed_url, feed_link)`
Main function that determines the appropriate favicon URL for a given feed.

**Parameters:**
- `feed_url`: The RSS feed URL
- `feed_link`: The website link from the feed (optional)

**Returns:**
- Favicon URL string or `None` if not found

#### `is_github_profile_feed(feed_url)`
Detects if a feed URL is a GitHub profile feed.

#### `extract_github_username(feed_url)`
Extracts the GitHub username from a GitHub feed URL.

#### `is_youtube_feed(feed_url)`
Detects if a feed URL is a YouTube channel feed.

#### `test_favicon_url(favicon_url)`
Tests if a favicon URL is accessible before using it.

### Error Handling
- Uses `onerror="this.style.display='none'"` to hide broken favicon images
- Graceful fallback when favicon detection fails
- Timeout protection for favicon requests (5 seconds)

## Usage Examples

### GitHub Profile Feeds
```xml
<outline text="Linus Torvalds" title="Linus Torvalds" type="rss"
         xmlUrl="https://github.com/torvalds.atom"
         htmlUrl="https://github.com/torvalds"
         category="GitHub"/>
```
Result: Uses `https://github.com/torvalds.png?size=50`

### Regular Website Feeds
```xml
<outline text="Hacker News" title="Hacker News" type="rss"
         xmlUrl="https://hnrss.org/frontpage"
         htmlUrl="https://news.ycombinator.com/"
         category="Technology"/>
```
Result: Uses `https://news.ycombinator.com/favicon.ico`

## Performance Considerations

- Favicon fetching happens during feed processing, not during page load
- Uses HEAD requests when possible to minimize bandwidth
- Implements retry logic with reasonable timeouts
- Favicon URLs are cached in feed metadata

## Testing

The feature includes comprehensive unit tests covering:
- GitHub profile feed detection
- Username extraction from GitHub URLs
- YouTube feed detection
- Special domain handling
- Favicon URL generation

Run tests with:
```bash
python -m pytest tests/test_utils.py -k favicon
```

## Browser Compatibility

The favicon feature works across all modern browsers and degrades gracefully:
- Icons are displayed when available
- Hidden automatically when URLs fail to load
- No JavaScript dependencies for basic functionality

## Future Enhancements

Potential improvements could include:
- Favicon caching to reduce repeated requests
- Support for more platform-specific icons
- Fallback to domain-based default icons
- Favicon size optimization for different display contexts