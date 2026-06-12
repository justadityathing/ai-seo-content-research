#!/usr/bin/env python3
"""
Fetch LinkedIn posts for AI-SEO content research using Apify.
Usage: python scripts/fetch_linkedin.py
Requires: pip install apify-client
Set environment variable: export APIFY_TOKEN=your_token_here
Reads scripts/profiles.csv with columns: author,linkedin_url
Saves posts to research/linkedin-posts/{author}.md
"""

import os
import csv
import time
from pathlib import Path
from datetime import datetime
from apify_client import ApifyClient

# Config
APIFY_TOKEN = os.environ.get('APIFY_TOKEN')
CSV_FILE = "scripts/profiles.csv"
OUTPUT_DIR = "research/linkedin-posts"
ACTOR_ID = "harvestapi/linkedin-profile-posts"

def get_linkedin_profile_url(input_url):
    """Normalize LinkedIn URL to profile URL."""
    url = input_url.strip()
    if not url.startswith('http'):
        url = f"https://www.linkedin.com/in/{url}/"
    if not url.endswith('/'):
        url += '/'
    return url

def fetch_linkedin_posts(profile_url):
    """Fetch posts from LinkedIn profile using Apify actor."""
    if not APIFY_TOKEN:
        print("  ✗ APIFY_TOKEN not set. Run: export APIFY_TOKEN=your_token")
        return []
    
    client = ApifyClient(APIFY_TOKEN)
    
    input_data = {
        "profileUrls": [profile_url],
        "maxPostsPerProfile": 15,
        "scrapeReactions": True,
        "scrapeComments": False,
    }
    
    try:
        print(f"  → Calling Apify actor {ACTOR_ID}...")
        run = client.actor(ACTOR_ID).call(run_input=input_data)
        
        dataset_id = run.get('datasetId')
        if not dataset_id:
            print(f"  ✗ No dataset returned from actor")
            return []
        
        items = client.dataset(dataset_id).list_items().items
        print(f"  ✓ Fetched {len(items)} posts from {profile_url}")
        return items
    except Exception as e:
        print(f"  ✗ Apify error: {str(e)}")
        return []

def save_linkedin_posts(author, posts):
    """Save posts to organized file."""
    author_slug = author.lower().replace(' ', '-').replace('ç', 'c')
    output_file = Path(OUTPUT_DIR) / f"{author_slug}.md"
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    content = f"# LinkedIn Posts: {author}\n\n"
    content += f"**Collection date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    content += f"**Total posts collected:** {len(posts)}\n\n"
    content += "---\n\n"
    
    # Sort by date descending (newest first)
    sorted_posts = sorted(posts, 
                         key=lambda x: x.get('postedAt', '1900-01-01'), 
                         reverse=True)
    
    for i, post in enumerate(sorted_posts, 1):
        date = post.get('postedAt', 'unknown date')[:10]  # YYYY-MM-DD
        text = post.get('content', '(no text)').strip()
        likes = post.get('likeCount', 0)
        comments = post.get('commentCount', 0)
        url = post.get('postUrl', '')
        
        # Truncate long posts
        if len(text) > 500:
            text = text[:500] + "...[truncated]"
        
        content += f"## Post #{i}\n\n"
        content += f"**Date:** {date}\n"
        content += f"**Reactions:** {likes} | **Comments:** {comments}\n"
        if url:
            content += f"**URL:** {url}\n"
        content += f"\n{text}\n\n"
        content += "---\n\n"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"  ✓ Saved: {output_file}")

def main():
    if not os.path.exists(CSV_FILE):
        print(f"Error: {CSV_FILE} not found.")
        print("Create it with columns: author,linkedin_url")
        print("Example:")
        print("  author,linkedin_url")
        print("  Ryan Law,https://www.linkedin.com/in/ryanlaw/")
        return
    
    with open(CSV_FILE, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    
    print(f"Found {len(rows)} profiles in {CSV_FILE}\n")
    
    for i, row in enumerate(rows):
        author = row.get('author', '').strip()
        linkedin_url = row.get('linkedin_url', '').strip()
        
        if not linkedin_url:
            print(f"  ✗ Row {i+2}: No linkedin_url, skipping")
            continue
        
        profile_url = get_linkedin_profile_url(linkedin_url)
        print(f"[{i+1}/{len(rows)}] {author}")
        
        posts = fetch_linkedin_posts(profile_url)
        if posts:
            save_linkedin_posts(author, posts)
        
        if i < len(rows) - 1:
            time.sleep(2)  # Rate limit between requests
    
    print(f"\n✓ Complete. Posts saved to {OUTPUT_DIR}/")

if __name__ == '__main__':
    main()
