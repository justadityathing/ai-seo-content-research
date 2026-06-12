#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fetch LinkedIn posts for AI-SEO content research using Apify.
Usage: APIFY_TOKEN=xxx python scripts/fetch_linkedin.py
Reads scripts/profiles-linkedin.csv
Saves to research/linkedin-posts/{author-slug}.md
Commits + pushes after each author.
"""
import os, csv, re, subprocess, sys
# Force UTF-8 stdout on Windows
if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')
from pathlib import Path
from datetime import datetime
from apify_client import ApifyClient

APIFY_TOKEN = os.environ.get('APIFY_TOKEN', '')
BASE_DIR = Path(__file__).resolve().parent.parent
CSV_FILE = BASE_DIR / 'scripts' / 'profiles-linkedin.csv'
OUT_DIR = BASE_DIR / 'research' / 'linkedin-posts'
ACTOR_ID = 'harvestapi/linkedin-profile-posts'
MAX_TEXT = 1500


def slugify(name):
    s = name.lower()
    s = re.sub(r'[^a-z0-9]+', '-', s)
    return s.strip('-')


def extract_text(post):
    for field in ('content', 'text', 'postText', 'description'):
        v = post.get(field)
        if isinstance(v, str) and v.strip():
            return v.strip()
    ca = post.get('contentAttributes') or {}
    for sub in ('text', 'content'):
        v = ca.get(sub) if isinstance(ca, dict) else None
        if isinstance(v, str) and v.strip():
            return v.strip()
    return '*(no text)*'


def extract_engagement(post):
    eng = post.get('engagement') or {}
    reactions = eng.get('numLikes') or eng.get('reactions') or post.get('reactions') or 0
    comments = eng.get('numComments') or eng.get('comments') or post.get('comments') or 0
    if isinstance(reactions, list):
        reactions = len(reactions)
    if isinstance(comments, list):
        comments = len(comments)
    return int(reactions or 0), int(comments or 0)


def extract_date(post):
    for f in ('postedAt', 'date', 'publishedAt', 'createdAt'):
        v = post.get(f)
        if v:
            return str(v)[:10]
    return 'unknown'


def extract_url(post):
    for f in ('linkedinUrl', 'shareLinkedinUrl', 'url', 'postUrl'):
        v = post.get(f)
        if v:
            return v
    return ''


def build_markdown(name, posts, collection_date):
    lines = [
        f'# LinkedIn Posts: {name}',
        f'**Collection date:** {collection_date}',
        f'**Total posts:** {len(posts)}',
        '', '---', '',
    ]
    for i, post in enumerate(posts, 1):
        text = extract_text(post)
        reactions, comments = extract_engagement(post)
        date = extract_date(post)
        url = extract_url(post)
        if len(text) > MAX_TEXT:
            text = text[:MAX_TEXT] + '... *(truncated)*'
        lines += [
            f'## Post #{i}',
            f'**Date:** {date}  ',
            f'**Reactions:** {reactions} | **Comments:** {comments}  ',
            f'**URL:** {url}',
            '',
            text,
            '', '---', '',
        ]
    return '\n'.join(lines)


def git_commit_push(name, count):
    subprocess.run(['git', 'add', 'research/linkedin-posts/'], cwd=BASE_DIR, check=True)
    msg = f'data: {name} — {count} linkedin posts'
    subprocess.run(['git', 'commit', '-m', msg], cwd=BASE_DIR, check=True)
    subprocess.run(['git', 'push'], cwd=BASE_DIR, check=True)
    print(f'  Committed & pushed: {msg}')


def main():
    if not APIFY_TOKEN:
        print('ERROR: Set APIFY_TOKEN env var')
        return

    client = ApifyClient(APIFY_TOKEN)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    collection_date = datetime.now().strftime('%Y-%m-%d')
    failures = []

    with open(CSV_FILE, encoding='utf-8') as f:
        rows = list(csv.DictReader(f))

    print(f'Processing {len(rows)} profiles...\n')

    for i, row in enumerate(rows):
        name = row.get('author', '').strip()
        url = row.get('linkedin_url', '').strip()
        slug = slugify(name)
        print(f'[{i+1}/{len(rows)}] {name}')

        try:
            run = client.actor(ACTOR_ID).call(run_input={
                'targetUrls': [url],
                'maxPosts': 15,
                'scrapeReactions': True,
            })
            posts = list(client.dataset(run.default_dataset_id).iterate_items())
            print(f'  Posts fetched: {len(posts)}')

            if not posts:
                print(f'  SKIP: 0 posts (profile may be private or inactive)')
                failures.append((name, '0 posts returned'))
                continue

            posts.sort(key=lambda p: str(p.get('postedAt', '')), reverse=True)
            md = build_markdown(name, posts, collection_date)
            out_path = OUT_DIR / f'{slug}.md'
            out_path.write_text(md, encoding='utf-8')
            print(f'  Saved: {out_path}')
            git_commit_push(name, len(posts))

        except Exception as e:
            print(f'  FAIL: {e}')
            failures.append((name, str(e)[:120]))

    print('\n=== DONE ===')
    if failures:
        print(f'Failures ({len(failures)}):')
        for name, reason in failures:
            print(f'  - {name}: {reason}')


if __name__ == '__main__':
    main()
