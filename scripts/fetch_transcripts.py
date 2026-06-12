#!/usr/bin/env python3
"""
Fetch YouTube transcripts for AI-SEO content research.
Usage: python scripts/fetch_transcripts.py
Reads scripts/videos.csv, fetches transcripts, saves to research/youtube-transcripts/{author}/
Requires: pip install youtube-transcript-api
"""

import csv
import os
import time
from pathlib import Path
from datetime import datetime
from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse, parse_qs

# Config
CSV_FILE = "scripts/videos.csv"
OUTPUT_DIR = "research/youtube-transcripts"
SLEEP_SECONDS = 2  # Rate limit: 2 seconds between requests

def extract_video_id(url):
    """Extract video ID from YouTube URL."""
    parsed = urlparse(url)
    if parsed.hostname in ('youtube.com', 'www.youtube.com'):
        return parse_qs(parsed.query).get('v', [None])[0]
    elif parsed.hostname == 'youtu.be':
        return parsed.path.lstrip('/')
    return None

def fetch_transcript(video_url):
    """Fetch transcript from YouTube URL. Returns dict or None on failure."""
    video_id = extract_video_id(video_url)
    if not video_id:
        print(f"  ✗ Could not extract video ID from {video_url}")
        return None
    
    try:
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
        transcript_text = '\n'.join([item['text'] for item in transcript_list])
        return {'video_id': video_id, 'transcript': transcript_text}
    except Exception as e:
        print(f"  ✗ Failed to fetch {video_url}: {str(e)}")
        return None

def save_transcript(author, title, date, transcript_text, video_url):
    """Save transcript to organized folder structure."""
    author_slug = author.lower().replace(' ', '-').replace('ğ', 'g').replace('ü', 'u').replace('ü', 'u')
    author_dir = Path(OUTPUT_DIR) / author_slug
    author_dir.mkdir(parents=True, exist_ok=True)
    
    date_slug = date.replace('/', '-') if date else 'no-date'
    title_slug = title[:40].lower().replace(' ', '-').replace('/', '-')
    filename = f"{date_slug}--{title_slug}.md"
    filepath = author_dir / filename
    
    content = f"""# {title}

**Author:** {author}  
**Video URL:** {video_url}  
**Date published:** {date}  
**Transcript fetched:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Why this matters
(Add your 1–2 sentence annotation here about what makes this video relevant to AI-powered SEO content production.)

---

## Transcript

{transcript_text}
"""
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"  ✓ Saved: {filepath}")

def main():
    if not os.path.exists(CSV_FILE):
        print(f"Error: {CSV_FILE} not found. Create it first with columns: author,video_url,title,date")
        return
    
    with open(CSV_FILE, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    
    print(f"Found {len(rows)} videos in {CSV_FILE}")
    
    for i, row in enumerate(rows):
        author = row.get('author', '').strip()
        video_url = row.get('video_url', '').strip()
        title = row.get('title', 'untitled').strip()
        date = row.get('date', '').strip()
        
        if not video_url:
            print(f"  ✗ Row {i+2}: No video_url, skipping")
            continue
        
        print(f"\n[{i+1}/{len(rows)}] Fetching: {title} ({author})")
        transcript = fetch_transcript(video_url)
        
        if transcript:
            save_transcript(author, title, date, transcript['transcript'], video_url)
        
        if i < len(rows) - 1:
            time.sleep(SLEEP_SECONDS)
    
    print(f"\n✓ Complete. Transcripts saved to {OUTPUT_DIR}/")

if __name__ == '__main__':
    main()
