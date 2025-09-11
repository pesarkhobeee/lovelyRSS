import sys
sys.path.append("scripts")
from scripts.fetch_feeds import RSSHub
import feedparser
import os
import shutil
import tempfile
import pytest

@pytest.fixture
def opml_file(tmp_path):
    return create_mock_opml_file(tmp_path)

@pytest.fixture
def config_file(tmp_path):
    return create_mock_config_file(tmp_path)

@pytest.fixture
def hub(opml_file, config_file, tmp_path):
    return create_mock_hub(opml_file, config_file, tmp_path)

def create_mock_opml_file(tmp_path):
    opml_content = '''
    <opml version="1.0">
        <body>
            <outline text="Feed 1" title="Feed 1" type="rss" xmlUrl="http://example.com/feed1.xml"/>
            <outline text="Feed 2" title="Feed 2" type="rss" xmlUrl="http://example.com/feed2.xml"/>
        </body>
    </opml>
    '''
    opml_file = tmp_path / "rss.opml"
    opml_file.write_text(opml_content)
    return str(opml_file)

def create_mock_config_file(tmp_path):
    config_content = '''
    {
        "site_title": "Test Site",
        "site_description": "Test Description",
        "site_link": "http://example.com",
        "generator": "TestGenerator/1.0",
        "output_files": {
            "rss": "test_rss.xml",
            "feeds": "test_feeds.xml",
            "json": "test_posts.json",
            "html": "test_index.html"
        },
        "max_entries": {
            "rss": 1,
            "json": 1,
            "html": 1
        }
    }
    '''
    config_file = tmp_path / "config.json"
    config_file.write_text(config_content)
    return str(config_file)

def create_mock_hub(opml_file, config_file, tmp_path):
    hub = RSSHub(opml_file=opml_file, config_file=config_file)
    hub.all_entries = [
        feedparser.FeedParserDict({
            'title': 'Entry 1',
            'link': 'http://example.com/entry1',
            'summary': 'Summary 1',
            'published': '2023-10-27T10:00:00Z',
            'feed_title': 'Feed 1',
            'feed_url': 'http://example.com/feed1.xml',
        }),
        feedparser.FeedParserDict({
            'title': 'Entry 2',
            'link': 'http://example.com/entry2',
            'summary': 'Summary 2',
            'published': '2023-10-26T10:00:00Z',
            'feed_title': 'Feed 2',
            'feed_url': 'http://example.com/feed2.xml',
        }),
    ]
    hub.feeds_with_updates = [
        {'title': 'Feed 1', 'url': 'http://example.com/feed1.xml'},
        {'title': 'Feed 2', 'url': 'http://example.com/feed2.xml'},
    ]
    os.chdir(tmp_path)
    return hub

def test_parse_opml(opml_file, config_file):
    hub = RSSHub(opml_file=opml_file, config_file=config_file)
    feeds = hub.parse_opml()
    assert len(feeds) == 2
    assert feeds[0]["title"] == "Feed 1"
    assert feeds[0]["url"] == "http://example.com/feed1.xml"
    assert feeds[1]["title"] == "Feed 2"
    assert feeds[1]["url"] == "http://example.com/feed2.xml"

def test_generate_latest_rss(hub):
    hub.generate_latest_rss()
    rss_file = hub.config["output_files"]["rss"]
    assert os.path.exists(rss_file)
    with open(rss_file, 'r') as f:
        content = f.read()
        assert "<title>Test Site</title>" in content
        assert "<link>http://example.com</link>" in content
        assert "<description>Test Description</description>" in content
        assert "<generator>TestGenerator/1.0</generator>" in content
        assert "<title>Entry 1</title>" in content
        assert "<title>Entry 2</title>" not in content

def test_generate_latest_feeds(hub):
    hub.generate_latest_feeds()
    feeds_file = hub.config["output_files"]["feeds"]
    assert os.path.exists(feeds_file)
    with open(feeds_file, 'r') as f:
        content = f.read()

        assert '<title>Feed 1</title>' in content

def test_generate_html(hub):
    hub.generate_html()
    html_file = hub.config["output_files"]["html"]
    assert os.path.exists(html_file)
    with open(html_file, 'r') as f:
        content = f.read()
        assert "<title>Test Site</title>" in content
        assert "<h1>🌟 Test Site</h1>" in content
        assert "<p>Test Description</p>" in content
        assert "Entry 1" in content
        assert "Entry 2" in content
