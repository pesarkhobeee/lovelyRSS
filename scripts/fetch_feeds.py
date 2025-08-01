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


from datetime import datetime, timezone, timedelta

import toml

class RSSHub:
    """Main RSS hub processor."""

    def __init__(self, opml_file: str = "feeds.opml", config_file: str = "config.json", last_run_file: str = "last_run.json"):
        # Determine which OPML file to use
        if os.path.exists(opml_file):
            self.opml_file = opml_file
        else:
            self.opml_file = "rss.opml.template"
            print(f"⚠️  {opml_file} not found, using {self.opml_file} as a fallback.")

        # Load configuration
        if os.path.exists(config_file):
            with open(config_file, 'r', encoding='utf-8') as f:
                self.config = json.load(f)
        else:
            with open("config.json.template", 'r', encoding='utf-8') as f:
                self.config = json.load(f)
            print(f"⚠️  {config_file} not found, using config.json.template as a fallback.")

        # Load version from pyproject.toml
        pyproject_path = Path(__file__).parent.parent / "pyproject.toml"
        with open(pyproject_path, "r") as f:
            pyproject = toml.load(f)
            self.version = pyproject["project"]["version"]

        self.last_run_file = last_run_file
        self.feeds = []
        self.all_entries = []
        self.feeds_with_updates = []
        
        # Setup Jinja2 environment
        template_dir = Path(__file__).parent.parent / "templates"
        self.jinja_env = Environment(
            loader=FileSystemLoader(template_dir),
            autoescape=True
        )

    def should_run(self) -> bool:
        """Check if the script should run based on the last run time."""
        if not os.path.exists(self.last_run_file):
            return True

        with open(self.last_run_file, 'r', encoding='utf-8') as f:
            last_run_data = json.load(f)
        
        last_run_time = datetime.fromisoformat(last_run_data["last_run"])
        update_interval = timedelta(hours=self.config.get("update_interval_hours", 6))

        return (datetime.now(timezone.utc) - last_run_time) >= update_interval

    def record_run(self):
        """Record the current run time."""
        with open(self.last_run_file, 'w', encoding='utf-8') as f:
            json.dump({"last_run": get_current_timestamp()}, f, indent=2)

    
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
                
                # Find the most recent entry date for this feed
                latest_entry_date = None
                latest_entry_parsed = None
                
                if parsed_feed.entries:
                    # Sort entries by publication date to find the latest
                    sorted_entries = sorted(
                        parsed_feed.entries,
                        key=lambda x: x.get('published_parsed') or (0,),
                        reverse=True
                    )
                    if sorted_entries:
                        latest_entry = sorted_entries[0]
                        latest_entry_date = safe_get_text(latest_entry, 'published')
                        latest_entry_parsed = latest_entry.get('published_parsed')
                
                # Store feed metadata
                feed_meta = {
                    'title': feed_info['title'],
                    'url': feed_info['url'],
                    'category': feed_info.get('category', ''),
                    'link': safe_get_text(parsed_feed.feed, 'link'),
                    'description': safe_get_text(parsed_feed.feed, 'description'),
                    'updated': safe_get_text(parsed_feed.feed, 'updated'),
                    'updated_parsed': parsed_feed.feed.get('updated_parsed'),
                    'latest_post_date': latest_entry_date,  # Most recent post date
                    'latest_post_parsed': latest_entry_parsed,  # Parsed version for sorting
                    'entry_count': len(parsed_feed.entries),
                    'language': safe_get_text(parsed_feed.feed, 'language', 'en'),
                }
                self.feeds_with_updates.append(feed_meta)
        
        if not self.all_entries:
            print("❌ No entries found in any feeds")
            sys.exit(1)
        
        print(f"📰 Total entries collected: {len(self.all_entries)}")
    
    def generate_latest_rss(self):
        """Generate merged RSS file with latest entries."""
        output_file = self.config["output_files"]["rss"]
        max_entries = self.config["max_entries"]["rss"]

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
        
        ET.SubElement(channel, 'title').text = self.config["site_title"]
        ET.SubElement(channel, 'description').text = self.config["site_description"]
        ET.SubElement(channel, 'link').text = self.config["site_link"]
        ET.SubElement(channel, 'lastBuildDate').text = get_readable_timestamp()
        ET.SubElement(channel, 'generator').text = self.config["generator"]
        
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
    
    def generate_latest_feeds(self):
        """Generate XML file with feeds sorted by recent updates."""
        output_file = self.config["output_files"]["feeds"]

        # Sort feeds by latest post date (more reliable than feed updated field)
        sorted_feeds = sorted(
            self.feeds_with_updates,
            key=lambda x: x.get('latest_post_parsed') or x.get('updated_parsed') or (0,),
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
    
    
    
    def generate_html(self):
        """Generate HTML page with feeds and latest entries."""
        output_file = self.config["output_files"]["html"]
        max_entries = self.config["max_entries"]["html"]

        # Sort entries by date
        sorted_entries = sorted(
            self.all_entries,
            key=lambda x: x.get('published_parsed') or (0,),
            reverse=True
        )
        latest_entries = sorted_entries[:max_entries]  # Show latest 30 on homepage
        
        # Sort feeds by update time (using latest post date)
        sorted_feeds = sorted(
            self.feeds_with_updates,
            key=lambda x: x.get('latest_post_parsed') or x.get('updated_parsed') or (0,),
            reverse=True
        )
        
        # Group feeds by category and sort within each category
        categories = {}
        for feed in sorted_feeds:
            category = feed.get('category') or 'Uncategorized'
            if category not in categories:
                categories[category] = []
            categories[category].append(feed)
        
        # Sort feeds within each category by most recent updates
        for category in categories:
            categories[category] = sorted(
                categories[category],
                key=lambda x: x.get('latest_post_parsed') or x.get('updated_parsed') or (0,),
                reverse=True
            )
        
        # Group entries by feed URL for easy access
        entries_by_feed = {}
        for entry in self.all_entries:
            feed_url = entry.get('feed_url')
            if feed_url not in entries_by_feed:
                entries_by_feed[feed_url] = []
            entries_by_feed[feed_url].append(entry)
        
        # Sort entries within each feed and limit to 10 latest
        for feed_url in entries_by_feed:
            entries_by_feed[feed_url] = sorted(
                entries_by_feed[feed_url],
                key=lambda x: x.get('published_parsed') or (0,),
                reverse=True
            )[:10]  # Keep only latest 10 posts per feed
        
        # Mark feeds with recent updates (last 24 hours)
        from datetime import datetime, timezone
        now = datetime.now(timezone.utc)
        one_day_ago = now.timestamp() - (24 * 60 * 60)
        
        for feed in sorted_feeds:
            if feed.get('latest_post_parsed'):
                import time
                post_timestamp = time.mktime(feed['latest_post_parsed'])
                feed['has_recent_update'] = post_timestamp > one_day_ago
            else:
                feed['has_recent_update'] = False
        
        # Prepare template data
        template_data = {
            'title': self.config["site_title"],
            'description': self.config["site_description"],
            'latest_entries': latest_entries,
            'feeds': sorted_feeds,
            'categories': categories,
            'entries_by_feed': entries_by_feed,
            'total_feeds': len(sorted_feeds),
            'total_entries': len(self.all_entries),
            'updated_time': get_readable_timestamp(),
            'update_interval_hours': self.config.get("update_interval_hours", 6),
            'version': self.version,
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

    if not hub.should_run():
        print("👋 Skipping run, not enough time has passed since the last run.")
        sys.exit(0)
    
    # Process all feeds
    hub.process_feeds()
    
    # Generate all output formats
    print("\n📄 Generating output files...")
    hub.generate_latest_rss()
    hub.generate_latest_feeds()
    hub.generate_html()

    hub.record_run()
    
    print("\n🎉 All files generated successfully!")
    print(f"📊 Summary: {len(hub.feeds_with_updates)} feeds, {len(hub.all_entries)} total entries")


if __name__ == "__main__":
    main()
