#!/usr/bin/env python3
"""
lovelyRSS - Personal GitHub-based RSS hub
Fetch and process RSS feeds from OPML file
"""

import json
import os
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Dict, List, Optional

import feedparser
from jinja2 import Environment, FileSystemLoader

from utils import (
    clean_html,
    fetch_with_retry,
    format_date,
    get_current_timestamp,
    get_readable_timestamp,
    safe_get_text,
    truncate_text,
    validate_url,
)


class RSSHub:
    """Main RSS hub processor."""
    
    def __init__(self, opml_file: str = "rss.opml"):
        self.opml_file = opml_file
        self.feeds = []
        self.all_entries = []
        self.feeds_with_updates = []
        
        # Setup Jinja2 environment
        template_dir = Path(__file__).parent.parent / "templates"
        self.jinja_env = Environment(
            loader=FileSystemLoader(template_dir),
            autoescape=True
        )
    
    def parse_opml(self) -> List[Dict[str, str]]:
        """
        Parse OPML file and extract RSS feed URLs.
        
        Returns:
            List of feed dictionaries with title and url
        """
        feeds = []
        
        if not os.path.exists(self.opml_file):
            print(f"❌ Error: {self.opml_file} not found")
            return feeds
        
        try:
            with open(self.opml_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            root = ET.fromstring(content)
            
            # Find all outline elements with xmlUrl attribute
            for outline in root.findall('.//outline[@xmlUrl]'):
                feed_url = outline.get('xmlUrl')
                title = outline.get('title') or outline.get('text', 'Unknown Feed')
                category = outline.get('category', '')
                
                if validate_url(feed_url):
                    feeds.append({
                        'title': title.strip(),
                        'url': feed_url.strip(),
                        'category': category.strip()
                    })
                else:
                    print(f"⚠️  Skipping invalid URL: {feed_url}")
        
        except ET.ParseError as e:
            print(f"❌ Error parsing OPML: {e}")
        except Exception as e:
            print(f"❌ Error reading OPML file: {e}")
        
        return feeds
    
    def fetch_feed(self, feed_info: Dict[str, str]) -> Optional[feedparser.FeedParserDict]:
        """
        Fetch and parse a single RSS feed.
        
        Args:
            feed_info: Dictionary with feed information
            
        Returns:
            Parsed feed data or None if failed
        """
        feed_url = feed_info['url']
        
        print(f"📡 Fetching: {feed_info['title']}")
        
        response = fetch_with_retry(feed_url)
        if not response:
            return None
        
        try:
            parsed = feedparser.parse(response.content)
            
            if parsed.bozo and parsed.bozo_exception:
                print(f"⚠️  Feed {feed_url} has parsing issues: {parsed.bozo_exception}")
            
            if not parsed.entries:
                print(f"⚠️  No entries found in {feed_url}")
            
            return parsed
        
        except Exception as e:
            print(f"❌ Error parsing feed {feed_url}: {e}")
            return None
    
    def process_feeds(self):
        """Process all feeds and collect entries."""
        self.feeds = self.parse_opml()
        
        if not self.feeds:
            print("❌ No valid feeds found in OPML file")
            sys.exit(1)
        
        print(f"📚 Found {len(self.feeds)} feeds")
        
        for feed_info in self.feeds:
            parsed_feed = self.fetch_feed(feed_info)
            
            if parsed_feed and parsed_feed.entries:
                # Process entries
                for entry in parsed_feed.entries:
                    # Add feed metadata to each entry
                    entry['feed_title'] = feed_info['title']
                    entry['feed_url'] = feed_info['url']
                    entry['feed_category'] = feed_info.get('category', '')
                
                self.all_entries.extend(parsed_feed.entries)
                
                # Store feed metadata
                feed_meta = {
                    'title': feed_info['title'],
                    'url': feed_info['url'],
                    'category': feed_info.get('category', ''),
                    'link': safe_get_text(parsed_feed.feed, 'link'),
                    'description': safe_get_text(parsed_feed.feed, 'description'),
                    'updated': safe_get_text(parsed_feed.feed, 'updated'),
                    'updated_parsed': parsed_feed.feed.get('updated_parsed'),
                    'entry_count': len(parsed_feed.entries),
                    'language': safe_get_text(parsed_feed.feed, 'language', 'en'),
                }
                self.feeds_with_updates.append(feed_meta)
        
        if not self.all_entries:
            print("❌ No entries found in any feeds")
            sys.exit(1)
        
        print(f"📰 Total entries collected: {len(self.all_entries)}")
    
    def generate_latest_rss(self, output_file: str = "latest_rss.xml", max_entries: int = 50):
        """Generate merged RSS file with latest entries."""
        # Sort entries by publication date (newest first)
        sorted_entries = sorted(
            self.all_entries,
            key=lambda x: x.get('published_parsed') or (0,),
            reverse=True
        )
        
        latest_entries = sorted_entries[:max_entries]
        
        # Create RSS XML
        rss = ET.Element('rss', version='2.0')
        rss.set('xmlns:atom', 'http://www.w3.org/2005/Atom')
        
        channel = ET.SubElement(rss, 'channel')
        
        ET.SubElement(channel, 'title').text = 'lovelyRSS - Latest Posts'
        ET.SubElement(channel, 'description').text = 'Latest posts from all subscribed feeds'
        ET.SubElement(channel, 'link').text = 'https://github.com'
        ET.SubElement(channel, 'lastBuildDate').text = get_readable_timestamp()
        ET.SubElement(channel, 'generator').text = 'lovelyRSS/1.0'
        
        # Add atom:link for self-reference
        atom_link = ET.SubElement(channel, '{http://www.w3.org/2005/Atom}link')
        atom_link.set('href', f'./{output_file}')
        atom_link.set('rel', 'self')
        atom_link.set('type', 'application/rss+xml')
        
        for entry in latest_entries:
            item = ET.SubElement(channel, 'item')
            ET.SubElement(item, 'title').text = safe_get_text(entry, 'title', 'No Title')
            ET.SubElement(item, 'link').text = safe_get_text(entry, 'link')
            ET.SubElement(item, 'description').text = clean_html(safe_get_text(entry, 'summary'))
            
            if entry.get('published'):
                ET.SubElement(item, 'pubDate').text = entry['published']
            
            # Add GUID
            guid = ET.SubElement(item, 'guid')
            guid.text = safe_get_text(entry, 'link') or safe_get_text(entry, 'id', 'no-guid')
            guid.set('isPermaLink', 'true' if entry.get('link') else 'false')
            
            # Add source feed info
            source = ET.SubElement(item, 'source')
            source.text = entry.get('feed_title', 'Unknown Feed')
            source.set('url', entry.get('feed_url', ''))
        
        # Write to file
        tree = ET.ElementTree(rss)
        ET.indent(tree, space="  ", level=0)
        tree.write(output_file, encoding='utf-8', xml_declaration=True)
        print(f"✅ Generated {output_file} with {len(latest_entries)} entries")
    
    def generate_latest_feeds(self, output_file: str = "latest_feeds.xml"):
        """Generate XML file with feeds sorted by recent updates."""
        # Sort feeds by last update time
        sorted_feeds = sorted(
            self.feeds_with_updates,
            key=lambda x: x.get('updated_parsed') or (0,),
            reverse=True
        )
        
        # Create feeds XML
        feeds_xml = ET.Element('feeds')
        feeds_xml.set('updated', get_current_timestamp())
        feeds_xml.set('count', str(len(sorted_feeds)))
        
        for feed in sorted_feeds:
            feed_elem = ET.SubElement(feeds_xml, 'feed')
            ET.SubElement(feed_elem, 'title').text = feed.get('title', 'Unknown Feed')
            ET.SubElement(feed_elem, 'url').text = feed.get('url', '')
            ET.SubElement(feed_elem, 'link').text = feed.get('link', '')
            ET.SubElement(feed_elem, 'description').text = feed.get('description', '')
            ET.SubElement(feed_elem, 'updated').text = feed.get('updated', '')
            ET.SubElement(feed_elem, 'entry_count').text = str(feed.get('entry_count', 0))
            ET.SubElement(feed_elem, 'category').text = feed.get('category', '')
            ET.SubElement(feed_elem, 'language').text = feed.get('language', 'en')
        
        # Write to file
        tree = ET.ElementTree(feeds_xml)
        ET.indent(tree, space="  ", level=0)
        tree.write(output_file, encoding='utf-8', xml_declaration=True)
        print(f"✅ Generated {output_file} with {len(sorted_feeds)} feeds")
    
    def generate_json_feed(self, output_file: str = "latest_posts.json", max_entries: int = 50):
        """Generate JSON feed for API consumption."""
        # Sort entries by publication date (newest first)
        sorted_entries = sorted(
            self.all_entries,
            key=lambda x: x.get('published_parsed') or (0,),
            reverse=True
        )
        
        latest_entries = sorted_entries[:max_entries]
        
        json_feed = {
            "version": "https://jsonfeed.org/version/1.1",
            "title": "lovelyRSS - Latest Posts",
            "description": "Latest posts from all subscribed feeds",
            "home_page_url": "https://github.com",
            "feed_url": f"./{output_file}",
            "items": []
        }
        
        for entry in latest_entries:
            item = {
                "id": safe_get_text(entry, 'link') or safe_get_text(entry, 'id', 'no-id'),
                "title": safe_get_text(entry, 'title', 'No Title'),
                "content_text": clean_html(safe_get_text(entry, 'summary')),
                "url": safe_get_text(entry, 'link'),
                "date_published": entry.get('published'),
                "external_url": safe_get_text(entry, 'link'),
                "tags": [entry.get('feed_category')] if entry.get('feed_category') else [],
                "_source": {
                    "feed_title": entry.get('feed_title', 'Unknown Feed'),
                    "feed_url": entry.get('feed_url', '')
                }
            }
            json_feed["items"].append(item)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(json_feed, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Generated {output_file} with {len(latest_entries)} entries")
    
    def generate_html(self, output_file: str = "index.html"):
        """Generate HTML page with feeds and latest entries."""
        # Sort entries by date
        sorted_entries = sorted(
            self.all_entries,
            key=lambda x: x.get('published_parsed') or (0,),
            reverse=True
        )
        latest_entries = sorted_entries[:30]  # Show latest 30 on homepage
        
        # Sort feeds by update time
        sorted_feeds = sorted(
            self.feeds_with_updates,
            key=lambda x: x.get('updated_parsed') or (0,),
            reverse=True
        )
        
        # Group feeds by category
        categories = {}
        for feed in sorted_feeds:
            category = feed.get('category') or 'Uncategorized'
            if category not in categories:
                categories[category] = []
            categories[category].append(feed)
        
        # Prepare template data
        template_data = {
            'title': 'lovelyRSS - Personal RSS Hub',
            'description': 'A personal RSS aggregator showcasing reading habits',
            'latest_entries': latest_entries,
            'feeds': sorted_feeds,
            'categories': categories,
            'total_feeds': len(sorted_feeds),
            'total_entries': len(self.all_entries),
            'updated_time': get_readable_timestamp(),
            'clean_html': clean_html,
            'format_date': format_date,
            'truncate_text': truncate_text,
        }
        
        # Render template
        template = self.jinja_env.get_template('index.html')
        html_content = template.render(**template_data)
        
        # Write to file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"✅ Generated {output_file}")


def main():
    """Main function to process all feeds."""
    print("🌟 lovelyRSS - Personal RSS Hub")
    print("=" * 40)
    
    # Initialize RSS hub
    hub = RSSHub()
    
    # Process all feeds
    hub.process_feeds()
    
    # Generate all output formats
    print("\n📄 Generating output files...")
    hub.generate_latest_rss()
    hub.generate_latest_feeds()
    hub.generate_json_feed()
    hub.generate_html()
    
    print("\n🎉 All files generated successfully!")
    print(f"📊 Summary: {len(hub.feeds_with_updates)} feeds, {len(hub.all_entries)} total entries")


if __name__ == "__main__":
    main()
