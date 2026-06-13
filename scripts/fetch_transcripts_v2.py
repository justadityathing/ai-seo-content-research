#!/usr/bin/env python3
"""
Fetch YouTube transcripts for AI-SEO content research.
Reads scripts/profiles-videos.csv, fetches transcripts with 3s delays,
saves to research/youtube-transcripts/{author-slug}/{date}--{title-slug}.md
After each author group, commits and pushes.
"""

import csv
import os
import re
import time
import subprocess
from pathlib import Path
from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse, parse_qs

CSV_FILE = "scripts/profiles-videos.csv"
OUTPUT_DIR = "research/youtube-transcripts"
SLEEP_SECONDS = 3


def extract_video_id(url):
    parsed = urlparse(url)
    if parsed.hostname in ('youtube.com', 'www.youtube.com'):
        return parse_qs(parsed.query).get('v', [None])[0]
    elif parsed.hostname == 'youtu.be':
        return parsed.path.lstrip('/')
    return None


def slugify(text, max_len=60):
    text = text.lower()
    # Handle special chars
    replacements = {'ğ': 'g', 'ü': 'u', 'ı': 'i', 'ş': 's', 'ö': 'o', 'ç': 'c'}
    for k, v in replacements.items():
        text = text.replace(k, v)
    text = re.sub(r'[^a-z0-9\s-]', '', text)
    text = re.sub(r'\s+', '-', text.strip())
    text = re.sub(r'-+', '-', text)
    return text[:max_len].rstrip('-')


def fetch_transcript(video_url):
    video_id = extract_video_id(video_url)
    if not video_id:
        print(f"  ✗ Could not extract video ID from {video_url}")
        return None
    try:
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
        transcript_text = ' '.join([item['text'] for item in transcript_list])
        return transcript_text
    except Exception as e:
        print(f"  ✗ Failed ({video_id}): {e}")
        return None


def save_transcript(author, title, date, url, transcript_text):
    author_slug = slugify(author)
    author_dir = Path(OUTPUT_DIR) / author_slug
    author_dir.mkdir(parents=True, exist_ok=True)

    title_slug = slugify(title, max_len=60)
    filename = f"{date}--{title_slug}.md"
    filepath = author_dir / filename

    content = f"""# {title}
**Author:** {author}
**URL:** {url}
**Date:** {date}
**Why this matters:**
---
## Transcript
{transcript_text}
"""
    filepath.write_text(content, encoding='utf-8')
    print(f"  ✓ Saved: {filepath}")
    return filepath


def git_commit_push(author, n):
    msg = f"data: {author} — {n} youtube transcript{'s' if n != 1 else ''}"
    subprocess.run(["git", "add", "research/youtube-transcripts/"], check=True)
    result = subprocess.run(
        ["git", "commit", "-m", msg],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        if "nothing to commit" in result.stdout or "nothing to commit" in result.stderr:
            print(f"  (nothing new to commit for {author})")
            return
        print(f"  ✗ Commit failed: {result.stderr}")
        return
    print(f"  ✓ Committed: {msg}")
    push = subprocess.run(["git", "push"], capture_output=True, text=True)
    if push.returncode == 0:
        print(f"  ✓ Pushed")
    else:
        print(f"  ✗ Push failed: {push.stderr}")


def main():
    with open(CSV_FILE, 'r', encoding='utf-8') as f:
        rows = list(csv.DictReader(f))

    print(f"Found {len(rows)} videos\n")

    # Group by author to commit per author
    from collections import OrderedDict
    authors = OrderedDict()
    for row in rows:
        author = row['author'].strip()
        authors.setdefault(author, []).append(row)

    total = sum(len(v) for v in authors.values())
    idx = 0

    for author, videos in authors.items():
        print(f"\n=== {author} ({len(videos)} videos) ===")
        saved_count = 0

        for row in videos:
            idx += 1
            title = row['title'].strip()
            url = row['video_url'].strip()
            date = row['date'].strip()

            print(f"\n[{idx}/{total}] {title}")
            transcript = fetch_transcript(url)

            if transcript:
                save_transcript(author, title, date, url, transcript)
                saved_count += 1

            if idx < total:
                print(f"  Waiting {SLEEP_SECONDS}s...")
                time.sleep(SLEEP_SECONDS)

        if saved_count > 0:
            git_commit_push(author, saved_count)
        else:
            print(f"  No transcripts saved for {author}, skipping commit")

    print("\n✓ Done.")


if __name__ == '__main__':
    main()
