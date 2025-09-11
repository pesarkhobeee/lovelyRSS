import pytest
from scripts.utils import (
    clean_html,
    validate_url,
    truncate_text,
    format_date,
    get_domain,
    sanitize_filename,
    get_favicon_url,
    is_github_profile_feed,
    extract_github_username,
    is_youtube_feed,
)

def test_clean_html():
    assert clean_html("<p>Hello</p>") == "Hello"
    assert clean_html("Hello<script>alert('xss')</script>") == "Hello"
    assert clean_html("  leading and trailing spaces  ") == "leading and trailing spaces"
    assert clean_html("multiple   spaces") == "multiple spaces"
    assert clean_html("&lt;p&gt;escaped&lt;/p&gt;") == "<p>escaped</p>"

def test_validate_url():
    assert validate_url("https://example.com") == True
    assert validate_url("http://example.com") == True
    assert validate_url("ftp://example.com") == True
    assert validate_url("example.com") == False
    assert validate_url("invalid-url") == False

def test_truncate_text():
    assert truncate_text("short text", 20) == "short text"
    assert truncate_text("this is a long text that needs to be truncated", 20) == "this is a long text..."
    assert truncate_text("another long text to truncate at a specific point", 30) == "another long text to truncate..."

def test_format_date():
    assert format_date("2023-10-27T10:00:00Z") == "October 27, 2023 at 10:00 UTC"
    assert format_date(None) == "Unknown date"
    assert format_date("invalid-date") == "invalid-date"

def test_get_domain():
    assert get_domain("https://www.example.com/path/to/page") == "www.example.com"
    assert get_domain("http://sub.domain.co.uk:8080") == "sub.domain.co.uk:8080"
    assert get_domain("invalid-url") == ""

def test_sanitize_filename():
    assert sanitize_filename("file with spaces") == "file_with_spaces"
    assert sanitize_filename("file/with/slashes") == "file_with_slashes"
    assert sanitize_filename('file\\with\\backslashes') == "file_with_backslashes"
    assert sanitize_filename('file:with:colons') == "file_with_colons"
    assert sanitize_filename('file*with*asterisks') == "file_with_asterisks"
    assert sanitize_filename('file?with?question?marks') == "file_with_question_marks"
    assert sanitize_filename('file"with"quotes') == "file_with_quotes"
    assert sanitize_filename('file<with<less<than') == "file_with_less_than"
    assert sanitize_filename('file>with>greater>than') == "file_with_greater_than"
    assert sanitize_filename('file|with|pipes') == "file_with_pipes"

def test_is_github_profile_feed():
    assert is_github_profile_feed("https://github.com/torvalds.atom") == True
    assert is_github_profile_feed("https://github.com/user/repo/commits/main.atom") == True
    assert is_github_profile_feed("https://github.blog/feed/") == False
    assert is_github_profile_feed("https://example.com/feed.atom") == False

def test_extract_github_username():

    assert extract_github_username("https://github.com/user/repo/commits/main.atom") == "user"
    assert extract_github_username("https://github.blog/feed/") == None
    assert extract_github_username("https://example.com/feed.atom") == None

def test_is_youtube_feed():
    assert is_youtube_feed("https://www.youtube.com/feeds/videos.xml?channel_id=UCsXVk37bltHxD1rDPwtNM8Q") == True
    assert is_youtube_feed("https://www.youtube.com/feeds/videos.xml?user=username") == True
    assert is_youtube_feed("https://youtube.com/feed") == False
    assert is_youtube_feed("https://example.com/feed.xml") == False

def test_get_favicon_url_github_profiles():
    # Test GitHub profile feeds get the user's profile image
    favicon_url = get_favicon_url("https://github.com/torvalds.atom", "https://github.com/torvalds")


    favicon_url = get_favicon_url("https://github.com/user/repo/commits/main.atom", "https://github.com/user/repo")
    assert favicon_url == "https://github.com/user.png?size=50"

def test_get_favicon_url_youtube():
    # Test YouTube feeds get YouTube favicon
    favicon_url = get_favicon_url("https://www.youtube.com/feeds/videos.xml?channel_id=UCsXVk37bltHxD1rDPwtNM8Q", "https://www.youtube.com/channel/UCsXVk37bltHxD1rDPwtNM8Q")
    assert favicon_url == "https://www.youtube.com/favicon.ico"

def test_get_favicon_url_special_domains():
    # Test special domain handling
    favicon_url = get_favicon_url("https://stackoverflow.blog/feed/", "https://stackoverflow.blog/")


    favicon_url = get_favicon_url("https://hnrss.org/frontpage", "https://news.ycombinator.com/")
    assert favicon_url == "https://news.ycombinator.com/favicon.ico"
