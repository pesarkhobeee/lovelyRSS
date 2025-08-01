import pytest
from scripts.utils import (
    clean_html,
    validate_url,
    truncate_text,
    format_date,
    get_domain,
    sanitize_filename,
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
