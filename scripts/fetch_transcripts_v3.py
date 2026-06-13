#!/usr/bin/env python3
"""
Fetch YouTube transcripts via yt-dlp (uses browser cookies to bypass IP blocks).
Reads scripts/profiles-videos.csv, saves to research/youtube-transcripts/
"""

import csv
import os
import re
import sys
import time
import tempfile
import subprocess
from pathlib import Path

CSV_FILE = "scripts/profiles-videos.csv"
OUTPUT_DIR = "research/youtube-transcripts"
SLEEP_SECONDS = 3
COOKIES_FILE = "scripts/youtube-cookies.txt"  # export from Chrome via "Get cookies.txt LOCALLY" extension


def slugify(text, max_len=60):
    text = text.lower()
    for k, v in {'g': 'g', 'u': 'u'}.items():
        pass
    replacements = {'ğ': 'g', '\xfc': 'u', 'ı': 'i', 'ş': 's', '\xf6': 'o', '\xe7': 'c'}
    for k, v in replacements.items():
        text = text.replace(k, v)
    text = re.sub(r'[^a-z0-9\s-]', '', text)
    text = re.sub(r'\s+', '-', text.strip())
    text = re.sub(r'-+', '-', text)
    return text[:max_len].rstrip('-')


def parse_vtt(vtt_text):
    """Strip VTT markup and de-duplicate overlapping captions."""
    lines = []
    seen = set()
    for line in vtt_text.splitlines():
        line = line.strip()
        if not line or '-->' in line or line.startswith('WEBVTT') or line.startswith('Kind:') or line.startswith('Language:'):
            continue
        # Strip tags like <00:00:01.000><c> etc.
        line = re.sub(r'<[^>]+>', '', line)
        line = re.sub(r'&amp;', '&', line)
        line = re.sub(r'&lt;', '<', line)
        line = re.sub(r'&gt;', '>', line)
        if line and line not in seen:
            seen.add(line)
            lines.append(line)
    return ' '.join(lines)


def fetch_transcript_ytdlp(video_url, cookies_file=COOKIES_FILE):
    """Use yt-dlp with cookies.txt to download auto-generated subtitles, return plain text."""
    with tempfile.TemporaryDirectory() as tmpdir:
        cmd = [
            "yt-dlp",
            "--cookies", cookies_file,
            "--write-auto-sub",
            "--skip-download",
            "--sub-lang", "en",
            "--sub-format", "vtt",
            "--output", os.path.join(tmpdir, "%(id)s"),
            "--no-playlist",
            "--quiet",
            video_url,
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        if result.returncode != 0:
            print(f"  FAIL yt-dlp: {result.stderr.strip()[:200]}")
            return None

        vtt_files = list(Path(tmpdir).glob("*.vtt"))
        if not vtt_files:
            print("  FAIL: no subtitle file downloaded")
            return None

        vtt_text = vtt_files[0].read_text(encoding='utf-8', errors='replace')
        return parse_vtt(vtt_text)


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
    print(f"  OK Saved: {filepath}")
    return filepath


def git_commit_push(author, n):
    msg = f"data: {author} - {n} youtube transcript{'s' if n != 1 else ''}"
    subprocess.run(["git", "add", "research/youtube-transcripts/"], check=True)
    result = subprocess.run(["git", "commit", "-m", msg], capture_output=True, text=True)
    if result.returncode != 0:
        out = result.stdout + result.stderr
        if "nothing to commit" in out:
            print(f"  (nothing new to commit for {author})")
            return
        print(f"  Commit failed: {result.stderr}")
        return
    print(f"  Committed: {msg}")
    push = subprocess.run(["git", "push"], capture_output=True, text=True)
    if push.returncode == 0:
        print(f"  Pushed OK")
    else:
        print(f"  Push failed: {push.stderr.strip()[:200]}")


def main():
    cookies_file = sys.argv[1] if len(sys.argv) > 1 else COOKIES_FILE

    if not os.path.exists(cookies_file):
        print(f"ERROR: cookies file not found: {cookies_file}")
        print("Export your YouTube cookies from Chrome using the 'Get cookies.txt LOCALLY' extension.")
        sys.exit(1)

    with open(CSV_FILE, 'r', encoding='utf-8') as f:
        rows = list(csv.DictReader(f))

    print(f"Found {len(rows)} videos. Using cookies: {cookies_file}\n")

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
            transcript = fetch_transcript_ytdlp(url, cookies_file)

            if transcript:
                save_transcript(author, title, date, url, transcript)
                saved_count += 1
            else:
                print(f"  Skipping {title}")

            if idx < total:
                print(f"  Waiting {SLEEP_SECONDS}s...")
                time.sleep(SLEEP_SECONDS)

        if saved_count > 0:
            git_commit_push(author, saved_count)
        else:
            print(f"  No transcripts saved for {author}, skipping commit")

    print("\nDone.")


if __name__ == '__main__':
    main()
