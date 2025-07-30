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
