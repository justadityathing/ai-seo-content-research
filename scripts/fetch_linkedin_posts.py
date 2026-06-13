#!/usr/bin/env python3
"""
Fetch LinkedIn posts for SEO experts via Apify actor harvestapi/linkedin-profile-posts.
Saves to research/linkedin-posts/{author-slug}.md, commits + pushes after each author.

Usage:
    python scripts/fetch_linkedin_posts.py
"""

import csv
import io
import os
import re
import subprocess
import sys
import time
from pathlib import Path

# Force UTF-8 output so Turkish chars don't crash on Windows cp1252 consoles
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

from apify_client import ApifyClient

APIFY_TOKEN = os.environ.get("APIFY_TOKEN", "")  # set via env var
ACTOR_ID = "harvestapi/linkedin-profile-posts"
MAX_POSTS = 15
CSV_FILE = "scripts/profiles-linkedin.csv"
OUTPUT_DIR = Path("research/linkedin-posts")
SLEEP_BETWEEN_AUTHORS = 5


def slugify(text: str) -> str:
    text = text.lower()
    for src, dst in {"ğ": "g", "ü": "u", "ı": "i", "ş": "s", "ö": "o", "ç": "c"}.items():
        text = text.replace(src, dst)
    text = re.sub(r"[^a-z0-9\s-]", "", text)
    text = re.sub(r"\s+", "-", text.strip())
    return re.sub(r"-+", "-", text)


def fetch_posts(client: ApifyClient, url: str) -> list[dict]:
    run = client.actor(ACTOR_ID).call(run_input={
        "targetUrls": [url],
        "maxPosts": MAX_POSTS,
    })
    if run is None:
        raise RuntimeError("Actor run returned None")
    dataset_id = run.default_dataset_id
    items = list(client.dataset(dataset_id).iterate_items())
    return items


def format_post(post: dict) -> str:
    date = post.get("postedAt") or post.get("date") or post.get("publishedAt") or "unknown"
    text = post.get("text") or post.get("content") or post.get("postText") or ""
    text = text.strip()
    reactions = (
        post.get("totalReactionCount")
        or post.get("reactions")
        or post.get("reactionCount")
        or post.get("numLikes")
        or 0
    )
    post_url = (
        post.get("postUrl")
        or post.get("url")
        or post.get("link")
        or post.get("shareUrl")
        or ""
    )
    lines = [
        f"**Date:** {date}",
        f"**Reactions:** {reactions}",
        f"**URL:** {post_url}",
        "",
        text,
        "",
        "---",
    ]
    return "\n".join(lines)


def save_posts(author: str, url: str, posts: list[dict]) -> Path:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    slug = slugify(author)
    filepath = OUTPUT_DIR / f"{slug}.md"
    header = f"# LinkedIn Posts — {author}\n**Profile:** {url}\n**Posts fetched:** {len(posts)}\n\n---\n\n"
    body = "\n".join(format_post(p) for p in posts)
    filepath.write_text(header + body, encoding="utf-8")
    print(f"  Saved {len(posts)} posts → {filepath}")
    return filepath


def git_commit_push(author: str, n: int) -> None:
    msg = f"data: {author} — linkedin posts"
    subprocess.run(["git", "add", str(OUTPUT_DIR)], check=True)
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


def main() -> None:
    client = ApifyClient(APIFY_TOKEN)

    with open(CSV_FILE, encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    print(f"Found {len(rows)} profiles\n")

    for i, row in enumerate(rows):
        author = row["author"].strip()
        url = row["linkedin_url"].strip()
        print(f"\n[{i+1}/{len(rows)}] {author}")
        print(f"  URL: {url}")

        try:
            posts = fetch_posts(client, url)
            print(f"  Fetched {len(posts)} posts")
            if posts:
                save_posts(author, url, posts)
                git_commit_push(author, len(posts))
            else:
                print("  No posts returned — skipping commit")
        except Exception as exc:
            print(f"  ERROR: {exc}")

        if i < len(rows) - 1:
            print(f"  Waiting {SLEEP_BETWEEN_AUTHORS}s before next author…")
            time.sleep(SLEEP_BETWEEN_AUTHORS)

    print("\nDone.")


if __name__ == "__main__":
    main()
