#!/usr/bin/env python3
"""
Fetch YouTube transcripts without cookies, using free APIs.
Methods tried in order per video:
  1. youtube-transcript-api (instance API, no cookies needed)
  2. youtubetranscript.com  (HTTP fallback, parse XML response)

Usage:
    python scripts/fetch_transcripts_v4.py
"""

import csv
import re
import time
import subprocess
from pathlib import Path
from urllib.parse import urlparse, parse_qs
from xml.etree import ElementTree

import requests

CSV_FILE = "scripts/profiles-videos.csv"
OUTPUT_DIR = "research/youtube-transcripts"
SLEEP_SECONDS = 15  # longer gap to reduce IP rate-limit risk

try:
    from youtube_transcript_api import YouTubeTranscriptApi as _YTApi
    _yt_api = _YTApi()
    YT_API_OK = True
except Exception:
    YT_API_OK = False


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def extract_video_id(url: str) -> str | None:
    parsed = urlparse(url)
    if parsed.hostname in ("youtube.com", "www.youtube.com"):
        return parse_qs(parsed.query).get("v", [None])[0]
    if parsed.hostname == "youtu.be":
        return parsed.path.lstrip("/")
    return None


def slugify(text: str, max_len: int = 60) -> str:
    text = text.lower()
    for src, dst in {"ğ": "g", "ü": "u", "ı": "i", "ş": "s", "ö": "o", "ç": "c"}.items():
        text = text.replace(src, dst)
    text = re.sub(r"[^a-z0-9\s-]", "", text)
    text = re.sub(r"\s+", "-", text.strip())
    text = re.sub(r"-+", "-", text)
    return text[:max_len].rstrip("-")


# ---------------------------------------------------------------------------
# Fetch methods
# ---------------------------------------------------------------------------

def fetch_via_yt_api(video_id: str) -> str | None:
    """youtube-transcript-api v0.6+ instance method — no cookies required."""
    if not YT_API_OK:
        return None
    try:
        transcript = _yt_api.fetch(video_id=video_id)
        text = " ".join(s.text for s in transcript)
        return text.strip() or None
    except Exception as exc:
        print(f"    [yt-api] {exc}")
        return None


def fetch_via_youtubetranscript_com(video_id: str) -> str | None:
    """
    Hits the youtubetranscript.com server-side XML endpoint as a backup.
    Returns a <transcript> XML doc with <text> children.
    """
    try:
        resp = requests.get(
            "https://youtubetranscript.com/",
            params={"server_vid_id": video_id},
            timeout=30,
            headers={"User-Agent": "Mozilla/5.0", "Accept": "application/xml, text/xml, */*"},
        )
        resp.raise_for_status()
        body = resp.text.strip()

        xml_start = body.find("<?xml")
        if xml_start == -1:
            xml_start = body.find("<transcript")
        if xml_start == -1:
            print("    [ytcom] no XML in response")
            return None

        root = ElementTree.fromstring(body[xml_start:])
        texts = [node.text or "" for node in root.iter("text")]
        transcript = " ".join(t.strip() for t in texts if t.strip())
        return transcript or None
    except Exception as exc:
        print(f"    [ytcom] {exc}")
        return None


def fetch_transcript(video_url: str) -> str | None:
    video_id = extract_video_id(video_url)
    if not video_id:
        print(f"  Could not extract video ID from {video_url}")
        return None

    print(f"  ID: {video_id}")

    print("  Trying youtube-transcript-api…")
    t = fetch_via_yt_api(video_id)
    if t:
        print(f"  [yt-api] OK ({len(t)} chars)")
        return t

    print("  Trying youtubetranscript.com…")
    t = fetch_via_youtubetranscript_com(video_id)
    if t:
        print(f"  [ytcom] OK ({len(t)} chars)")
        return t

    print("  All methods failed — skipping")
    return None


# ---------------------------------------------------------------------------
# I/O
# ---------------------------------------------------------------------------

def save_transcript(author: str, title: str, date: str, url: str, text: str) -> Path:
    author_dir = Path(OUTPUT_DIR) / slugify(author)
    author_dir.mkdir(parents=True, exist_ok=True)
    filepath = author_dir / f"{date}--{slugify(title)}.md"
    filepath.write_text(
        f"# {title}\n**Author:** {author}\n**URL:** {url}\n**Date:** {date}\n"
        f"**Why this matters:**\n---\n## Transcript\n{text}\n",
        encoding="utf-8",
    )
    print(f"  Saved: {filepath}")
    return filepath


def git_commit_push(author: str, n: int) -> None:
    msg = f"data: {author} — {n} youtube transcript{'s' if n != 1 else ''}"
    subprocess.run(["git", "add", "research/youtube-transcripts/"], check=True)
    result = subprocess.run(["git", "commit", "-m", msg], capture_output=True, text=True)
    if result.returncode != 0:
        out = result.stdout + result.stderr
        if "nothing to commit" in out:
            print(f"  (nothing new to commit for {author})")
        else:
            print(f"  Commit failed: {result.stderr.strip()[:300]}")
        return
    print(f"  Committed: {msg}")
    push = subprocess.run(["git", "push"], capture_output=True, text=True)
    if push.returncode == 0:
        print("  Pushed OK")
    else:
        print(f"  Push failed: {push.stderr.strip()[:300]}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    if YT_API_OK:
        print("youtube-transcript-api loaded OK (primary method)")
    else:
        print("youtube-transcript-api not available — will use youtubetranscript.com only")

    with open(CSV_FILE, encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    print(f"Found {len(rows)} videos\n")

    from collections import OrderedDict
    authors: dict[str, list] = OrderedDict()
    for row in rows:
        authors.setdefault(row["author"].strip(), []).append(row)

    total = sum(len(v) for v in authors.values())
    idx = 0

    for author, videos in authors.items():
        print(f"\n=== {author} ({len(videos)} videos) ===")
        saved = 0

        for row in videos:
            idx += 1
            title = row["title"].strip()
            url = row["video_url"].strip()
            date = row["date"].strip()

            print(f"\n[{idx}/{total}] {title}")

            # Skip if file already exists
            out_path = Path(OUTPUT_DIR) / slugify(author) / f"{date}--{slugify(title)}.md"
            if out_path.exists():
                print(f"  Already saved — skipping")
                continue

            transcript = fetch_transcript(url)

            if transcript:
                save_transcript(author, title, date, url, transcript)
                saved += 1
            else:
                print(f"  Skipped: {title}")

            if idx < total:
                print(f"  Waiting {SLEEP_SECONDS}s…")
                time.sleep(SLEEP_SECONDS)

        if saved:
            git_commit_push(author, saved)
        else:
            print(f"  No transcripts saved for {author} — skipping commit")

    print("\nDone.")


if __name__ == "__main__":
    main()
