"""
Utility functions for RSS processing
"""

import re
import html
from datetime import datetime, timezone
from typing import Dict, List, Optional, Union
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup


def clean_html(text: str) -> str:
    """
    Clean HTML content for display.

    Args:
        text: Raw HTML text

    Returns:
        Cleaned plain text
    """
    if not text:
        return ""

    # Use BeautifulSoup for better HTML cleaning
    soup = BeautifulSoup(text, 'html.parser')

    # Remove script and style elements
    for script in soup(["script", "style"]):
        script.decompose()

    # Get text and clean up
    clean_text = soup.get_text()

    # Decode HTML entities
    clean_text = html.unescape(clean_text)

    # Clean up whitespace
    clean_text = re.sub(r'\s+', ' ', clean_text).strip()

    return clean_text


def safe_get_text(element: Dict, key: str, default: str = "") -> str:
    """
    Safely get text from feed element.

    Args:
        element: Feed element dictionary
        key: Key to extract
        default: Default value if key not found

    Returns:
        Text content or default
    """
    value = element.get(key, default)
    if isinstance(value, str):
        return value
    return str(value) if value else default


def format_date(date_str: Optional[str]) -> str:
    """
    Format date string for display.

    Args:
        date_str: Date string from feed

    Returns:
        Formatted date string
    """
    if not date_str:
        return "Unknown date"

    try:
        # Try to parse and reformat with timezone handling
        from dateutil import parser
        # Define timezone mappings for common abbreviations
        tzinfos = {
            'UT': timezone.utc,
            'UTC': timezone.utc,
            'GMT': timezone.utc,
        }
        dt = parser.parse(date_str, tzinfos=tzinfos)
        return dt.strftime("%B %d, %Y at %H:%M UTC")
    except Exception:
        return date_str


def truncate_text(text: str, max_length: int = 200) -> str:
    """
    Truncate text to specified length with ellipsis.

    Args:
        text: Text to truncate
        max_length: Maximum length

    Returns:
        Truncated text
    """
    if len(text) <= max_length:
        return text

    # Find the last space before max_length
    truncated = text[:max_length]
    last_space = truncated.rfind(' ')

    if last_space > max_length * 0.8:  # If space is reasonably close to end
        truncated = truncated[:last_space]

    return truncated + "..."


def validate_url(url: str) -> bool:
    """
    Validate if a URL is well-formed.

    Args:
        url: URL to validate

    Returns:
        True if valid, False otherwise
    """
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except Exception:
        return False


def get_domain(url: str) -> str:
    """
    Extract domain from URL.

    Args:
        url: Full URL

    Returns:
        Domain name
    """
    try:
        parsed = urlparse(url)
        return parsed.netloc
    except Exception:
        return "unknown"


def fetch_with_retry(url: str, timeout: int = 10, retries: int = 3) -> Optional[requests.Response]:
    """
    Fetch URL with retry logic.

    Args:
        url: URL to fetch
        timeout: Request timeout in seconds
        retries: Number of retry attempts

    Returns:
        Response object or None if failed
    """
    headers = {
        'User-Agent': 'lovelyRSS/1.0 (RSS aggregator; +https://github.com/your-username/rss)'
    }


    headers['Accept'] = 'application/atom+xml'

    for attempt in range(retries):
        try:
            response = requests.get(url, timeout=timeout, headers=headers)
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            if attempt == retries - 1:  # Last attempt
                print(f"Failed to fetch {url} after {retries} attempts: {e}")
                return None
            print(f"Attempt {attempt + 1} failed for {url}: {e}")

    return None


def get_current_timestamp() -> str:
    """
    Get current timestamp in ISO format.

    Returns:
        Current timestamp string
    """
    return datetime.now(timezone.utc).isoformat()


def get_readable_timestamp() -> str:
    """
    Get current timestamp in readable format.

    Returns:
        Readable timestamp string
    """
    return datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')


def sanitize_filename(filename: str) -> str:
    """
    Sanitize filename for safe file system usage.

    Args:
        filename: Original filename

    Returns:
        Sanitized filename
    """
    # Remove or replace unsafe characters
    sanitized = re.sub(r'[<>:"/\\|?*]', '_', filename)
    sanitized = re.sub(r'\s+', '_', sanitized)
    return sanitized[:255]  # Limit length


def get_favicon_url(feed_url: str, feed_link: Optional[str] = None) -> Optional[str]:
    """
    Fetch favicon URL for a given feed.

    Args:
        feed_url: RSS feed URL
        feed_link: Website link from feed (optional)

    Returns:
        Favicon URL or None if not found
    """
    # Special handling for GitHub profile feeds
    if is_github_profile_feed(feed_url):
        username = extract_github_username(feed_url)
        if username:
            return f"https://github.com/{username}.png?size=50"

    # Special handling for YouTube feeds
    if is_youtube_feed(feed_url):
        return "https://www.youtube.com/favicon.ico"

    # Special handling for common platforms
    if feed_link:
        domain = get_domain(feed_link)
        if "stackoverflow.com" in domain:
            return "https://cdn.sstatic.net/Sites/stackoverflow/Img/favicon.ico"
        elif "news.ycombinator.com" in domain:
            return "https://news.ycombinator.com/favicon.ico"

    # Use feed_link if available, otherwise derive from feed_url
    base_url = feed_link if feed_link else feed_url

    try:
        parsed = urlparse(base_url)
        base_domain = f"{parsed.scheme}://{parsed.netloc}"

        # Try common favicon locations
        favicon_candidates = [
            urljoin(base_domain, "/favicon.ico"),
            urljoin(base_domain, "/favicon.png"),
            urljoin(base_domain, "/apple-touch-icon.png"),
        ]

        # Try to fetch the website and look for favicon in HTML
        try:
            response = fetch_with_retry(base_url, timeout=5)
            if response and response.text:
                # Use XML parser if it looks like XML, otherwise HTML parser
                parser = 'xml' if response.text.strip().startswith('<?xml') else 'html.parser'
                soup = BeautifulSoup(response.text, parser)

                # Look for favicon link tags
                favicon_links = soup.find_all('link', rel=lambda x: x and 'icon' in x.lower())
                for link in favicon_links:
                    href = link.get('href')
                    if href:
                        favicon_url = urljoin(base_domain, href)
                        favicon_candidates.insert(0, favicon_url)
        except Exception:
            pass  # Continue with default candidates

        # Test each candidate
        for favicon_url in favicon_candidates:
            if test_favicon_url(favicon_url):
                return favicon_url

    except Exception as e:
        print(f"Error getting favicon for {feed_url}: {e}")

    return None


def is_github_profile_feed(feed_url: str) -> bool:
    """
    Check if the feed URL is a GitHub profile feed.

    Args:
        feed_url: RSS feed URL

    Returns:
        True if it's a GitHub profile feed
    """
    return "github.com" in feed_url and (".atom" in feed_url or "/commits/" in feed_url)


def is_youtube_feed(feed_url: str) -> bool:
    """
    Check if the feed URL is a YouTube feed.

    Args:
        feed_url: RSS feed URL

    Returns:
        True if it's a YouTube feed
    """
    return "youtube.com" in feed_url and "feeds/videos.xml" in feed_url


def extract_github_username(feed_url: str) -> Optional[str]:
    """
    Extract GitHub username from a GitHub feed URL.

    Args:
        feed_url: GitHub feed URL

    Returns:
        Username or None if not found
    """
    try:
        # Common GitHub feed patterns:
        # https://github.com/username.atom
        # https://github.com/username/repo/commits/branch.atom
        if ".atom" in feed_url:
            if "/commits/" in feed_url:
                # Extract from repo feed
                match = re.search(r'github\.com/([^/]+)/', feed_url)
            else:
                # Extract from user feed
                match = re.search(r'github\.com/([^/.]+)\.atom', feed_url)

            if match:
                return match.group(1)
    except Exception:
        pass

    return None


def test_favicon_url(favicon_url: str) -> bool:
    """
    Test if a favicon URL is accessible.

    Args:
        favicon_url: URL to test

    Returns:
        True if accessible, False otherwise
    """
    try:
        headers = {
            'User-Agent': 'lovelyRSS/1.0 (RSS aggregator; favicon check)'
        }
        response = requests.head(favicon_url, timeout=3, headers=headers)
        return response.status_code == 200
    except Exception:
        return False
