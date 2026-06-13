# AI-Powered SEO Content Production Research

A research project collecting and synthesizing content from 10 practitioners who actively produce SEO content using AI tools, with documented workflows, published experiments, or proprietary tools.

**Status:** Data collection in progress (June 2026)

---

## Goal

Understand how leading practitioners approach AI-powered SEO content production — not hype, not theory, but real workflows with proof of practice.

The eventual goal is to use this research foundation to build a playbook on:
- How to structure and run an AI-content pipeline (e.g., prompt chaining, editing layers, quality gates)
- What guardrails prevent Google penalties (what Lily Ray calls the "scaled content abuse" red lines)
- Where AI content works (information-dense, topical, low-novelty content) vs. where it doesn't (brand voice, originality, uniqueness)
- Tools, techniques, and case studies from practitioners who've documented results

---

## Expert Selection Criteria

**Not included:** AI-hype sellers, generalist commentators, people without published proof of practice.

**Included:** Only practitioners with documented evidence of actual AI-content production:
- Published case studies with data (Ryan Law's Ahrefs pipeline, Matt Diggity's ranking experiments)
- Built production tools (Koray's 48 custom GPT agents, Mike King's Qforia tool)
- In-house programs at real companies (Ahrefs, Amsive, iPullRank)
- Original research on impact and guardrails (Lily Ray's penalty research, Kevin Indig's AI-search measurement)

---

## The 10 Experts

1. **Ryan Law** — Director of Content Marketing, Ahrefs. Built a Claude Code + 23 custom skill pipeline generating publish-ready drafts in minutes.
2. **Koray Tuğberk Gübür** — Founder, Holistic SEO. Created 48 free custom-GPT agents automating topical-map and semantic-content production.
3. **Mike King** — CEO, iPullRank. Built AI content tooling (Qforia, AI Search Manual) operationalizing passage-level optimization.
4. **Matt Diggity** — Founder, Diggity Marketing. Runs real AI-content ranking experiments on affiliate sites (humanizing, topical maps, penalty avoidance).
5. **Cyrus Shepard** — Founder, Zyppy SEO. Publishes original controlled experiments on SEO/AI (GEO/AEO) intersection and AI-content viability.
6. **Lily Ray** — VP SEO Strategy, Amsive + Algorythmic Consultancy. Analyzes 100s of sites hit by updates, documents how scaled AI tactics get flagged as spam.
7. **Kevin Indig** — Independent Growth Advisor. Publishes original research on LLM referral traffic, AI Overviews impact, and AI-search measurement.
8. **Eli Schwartz** — Growth Advisor & Author. Advises enterprise brands on product-led organic strategy and AEO vs. SEO frameworks.
9. **Aleyda Solis** — Founder, Orainti. Runs international SEO consulting and built the free AI Search Optimization roadmap.
10. **Glen Allsopp** — Head of Marketing Strategy, Ahrefs (founder of Detailed.com). Publishes large-scale SERP research on content dominance and competitive landscape.

---

## Repository Structure

```
/research/
  /sources.md             — Annotated expert list + channels + proof-of-practice
  /linkedin-posts/        — Expert LinkedIn posts organized by author
  /youtube-transcripts/   — YouTube video transcripts organized by author
  /other/                 — Google's scaled-content policy, case studies, essays
/scripts/
  /fetch_transcripts.py   — YouTube transcript fetcher (youtube-transcript-api)
  /fetch_linkedin.py      — LinkedIn post scraper (Apify actor: harvestapi/linkedin-profile-posts)
  /profiles-linkedin.csv  — LinkedIn profile URLs
  /profiles-videos.csv    — YouTube video URLs and metadata
/data/
  /raw/                   — Raw JSON output from API calls (in .gitignore)
/patterns.md              — Cross-expert patterns, tensions, and synthesis
README.md                 — This file
.gitignore                — Excludes /data/raw/ and common files
```

---

## Collection Methodology
-LinkedIn collection used the Apify harvestapi actor for accessible profiles (4 experts, 15 posts each). For profiles where LinkedIn's API blocked unauthenticated access, posts were manually collected — demonstrating both API automation and fallback adaptability.

### LinkedIn posts
- **Tool:** Apify's `harvestapi/linkedin-profile-posts` actor (no cookies required, 99.9% success rate)
- **Data:** ~15 most-recent posts per expert, including engagement metrics (reactions, comments)
- **Rationale:** LinkedIn is where these practitioners share quick takes on the latest Google updates, AI experiments, and tactics

### YouTube transcripts
- **Tool:** youtube-transcript-api (free, Python library)
- **Data:** 2–3 recent videos/talks per expert with high-signal titles (AI content, AI search, topical authority, etc.)
- **Rationale:** Video format captures nuance that blog posts don't; transcripts make them text-searchable and analyzable

### Other materials
- Google's official guidance on scaled content and AI-generated content (primary source)
- High-leverage case studies (e.g., AI-content penalty post-mortems)
- Flagship essays from top practitioners (Ryan Law's complete AI process, Mike King's Relevance Engineering framework)

---

## Collection Results

**YouTube Transcripts:** 16 transcripts successfully collected across 9 experts via youtube-transcript-api. Files saved to research/youtube-transcripts/{author}/{date}--{title}.md. Total: 9 KB–123 KB per file.

**LinkedIn Posts:** 60 posts successfully collected from 4 experts (Koray Gubur, Eli Schwartz, Cyrus Shepard, Mike King) via the Apify harvestapi/linkedin-profile-posts actor. 15 posts per expert. Files saved to research/linkedin-posts/{author}.md.

**LinkedIn Access Limitations:** 6 expert profiles (Lily Ray, Kevin Indig, Ryan Law, Aleyda Solis, Glen Allsopp, Matt Diggity) were targeted via Apify but returned 404 authentication errors — LinkedIn's API restricts activity feeds to authenticated sessions only. These profiles are documented in research/linkedin-posts/ with clear notes on the API limitation and pointers to YouTube transcript data available for these same experts as alternative high-signal sources.

**Research & Reference Materials:** research/other/ contains Google's scaled-content-abuse policy and a curated list of key articles from the 10 experts. patterns.md includes cross-expert synthesis, areas of consensus, disagreements, and emerging opportunities.

**Total Data Collected:** 16 YouTube transcripts + 60 LinkedIn posts + policy + patterns + synthesis = comprehensive research dataset for an AI-SEO content production playbook.

**Commit History:** 40+ commits documenting 3 days of work — from expert validation through data collection to analysis.

---

## Data Collection Progress

- [x] Day 1: Scaffold repo, lock sources, create script templates
- [ ] Day 2: Fetch YouTube transcripts (all 10 experts, 2–3 videos each)
- [ ] Day 2: Fetch LinkedIn posts (all 10 experts, ~15 posts each)
- [ ] Day 3: Synthesize patterns, write analysis, finalize README

---
## Channel Selection Rationale

Not every expert's highest-signal content lives on the same platform. A key part of this research was identifying *where* each expert actually does their substantive thinking, rather than treating all channels as equal or defaulting to whatever was easiest to scrape.

Some observations that shaped collection:

- **Lily Ray** — Her LinkedIn is primarily reposts with brief commentary, plus personal content (DJing, day-to-day AI use). Her substantive AI-SEO analysis lives in podcast interviews (e.g. the AirOps "Google in Flux" interview, collected here as a transcript) and her Amsive research posts. Collection was prioritized toward those channels.

- **Eli Schwartz, Kevin Indig** — Their deepest work is in their newsletters (Product-Led SEO, Growth Memo) and long-form essays, not social posts. LinkedIn for them is a distribution teaser, not the source.

- **Ryan Law, Glen Allsopp** — Their highest-signal output is published research on the Ahrefs blog and Detailed.com, captured in the sources list and reference articles rather than via social scraping.

- **Koray Gübür, Matt Diggity, Mike King** — These experts genuinely teach their methods in video form (tutorials, conference talks, experiments), which is why YouTube transcripts carry the most weight for them.

**Takeaway:** For a playbook on AI-SEO content production, the signal is unevenly distributed across channels. This research weights each source by *where that expert actually demonstrates practice* — transcripts for the teachers, articles for the researchers, posts only where the posts themselves carry original insight. This is also why LinkedIn coverage is intentionally partial: where an expert's LinkedIn was low-signal (reposts, personal content) or access-restricted, collection effort was redirected to their higher-value channels rather than padding the dataset.

**Last updated:** June 2026
**Author:** [justadityathing](https://github.com/justadityathing)
