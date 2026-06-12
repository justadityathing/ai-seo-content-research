# ai-seo-content-research
AI-Powered SEO Content Production Research
A research project collecting and synthesizing content from 10 practitioners who actively produce SEO content using AI tools, with documented workflows, published experiments, or proprietary tools.
Status: Data collection in progress (June 2026)
---
Goal
Understand how leading practitioners approach AI-powered SEO content production — not hype, not theory, but real workflows with proof of practice.
The eventual goal is to use this research foundation to build a playbook on:
How to structure and run an AI-content pipeline (e.g., prompt chaining, editing layers, quality gates)
What guardrails prevent Google penalties (what Lily Ray calls the "scaled content abuse" red lines)
Where AI content works (information-dense, topical, low-novelty content) vs. where it doesn't (brand voice, originality, uniqueness)
Tools, techniques, and case studies from practitioners who've documented results
---
Expert Selection Criteria
Not included: AI-hype sellers, generalist commentators, people without published proof of practice.
Included: Only practitioners with documented evidence of actual AI-content production:
Published case studies with data (Ryan Law's Ahrefs pipeline, Matt Diggity's ranking experiments)
Built production tools (Koray's 48 custom GPT agents, Mike King's Qforia tool)
In-house programs at real companies (Ahrefs, Amsive, iPullRank)
Original research on impact and guardrails (Lily Ray's penalty research, Kevin Indig's AI-search measurement)
---
The 10 Experts
Ryan Law — Director of Content Marketing, Ahrefs. Built a Claude Code + 23 custom skill pipeline generating publish-ready drafts in minutes.
Koray Tuğberk Gübür — Founder, Holistic SEO. Created 48 free custom-GPT agents automating topical-map and semantic-content production.
Mike King — CEO, iPullRank. Built AI content tooling (Qforia, AI Search Manual) operationalizing passage-level optimization.
Matt Diggity — Founder, Diggity Marketing. Runs real AI-content ranking experiments on affiliate sites (humanizing, topical maps, penalty avoidance).
Cyrus Shepard — Founder, Zyppy SEO. Publishes original controlled experiments on SEO/AI (GEO/AEO) intersection and AI-content viability.
Lily Ray — VP SEO Strategy, Amsive + Algorythmic Consultancy. Analyzes 100s of sites hit by updates, documents how scaled AI tactics get flagged as spam.
Kevin Indig — Independent Growth Advisor. Publishes original research on LLM referral traffic, AI Overviews impact, and AI-search measurement.
Eli Schwartz — Growth Advisor & Author. Advises enterprise brands on product-led organic strategy and AEO vs. SEO frameworks.
Aleyda Solis — Founder, Orainti. Runs international SEO consulting and built the free AI Search Optimization roadmap.
Glen Allsopp — Head of Marketing Strategy, Ahrefs (founder of Detailed.com). Publishes large-scale SERP research on content dominance and competitive landscape.
---
Repository Structure
```
/research/
  /sources.md                 — Annotated expert list + channels + proof-of-practice
  /linkedin-posts/            — Expert LinkedIn posts organized by author
  /youtube-transcripts/       — YouTube video transcripts organized by author
  /other/                     — Google's scaled-content policy, case studies, essays
/scripts/
  /fetch_transcripts.py       — YouTube transcript fetcher (youtube-transcript-api)
  /fetch_linkedin.py          — LinkedIn post scraper (Apify actor: harvestapi/linkedin-profile-posts)
  /profiles-linkedin.csv      — LinkedIn profile URLs
  /profiles-videos.csv        — YouTube video URLs and metadata
/data/
  /raw/                       — Raw JSON output from API calls (in .gitignore)
/patterns.md                  — Cross-expert patterns, tensions, and synthesis
README.md                      — This file
.gitignore                     — Excludes /data/raw/ and common files
```
---
Collection Methodology
LinkedIn posts
Tool: Apify's `harvestapi/linkedin-profile-posts` actor (no cookies required, 99.9% success rate)
Data: ~15 most-recent posts per expert, including engagement metrics (reactions, comments)
Cost: ~$0.30 total (covered by Apify free monthly credit)
Rationale: LinkedIn is where these practitioners share quick takes on the latest Google updates, AI experiments, and tactics
YouTube transcripts
Tool: youtube-transcript-api (free, Python library)
Data: 2–3 recent videos/talks per expert with high-signal titles (AI content, AI search, topical authority, etc.)
Rationale: Video format captures nuance that blog posts don't; transcripts make them text-searchable and analyzable
Other materials
Google's official guidance on scaled content and AI-generated content (primary source, not pundit interpretation)
High-leverage case studies (e.g., the Causal AI-content penalty, aftermath and lessons)
Flagship essays from top practitioners (e.g., Ryan Law's complete AI process, Mike King's Relevance Engineering framework)
---
Key Questions This Research Answers
What does an actual AI-content pipeline look like? (Ryan Law + Mike King)
How do you avoid Google penalties when running scaled AI content? (Lily Ray + Cyrus Shepard + Matt Diggity experiments)
Where does AI content actually work in SEO? (Information-dense, topical, low-novelty queries vs. brand/originality-dependent niches)
What's the difference between AEO (AI Engine Optimization) and SEO? (Eli Schwartz + Kevin Indig's research)
What are practitioners learning from AI Overviews and how do they adapt content strategy? (Lily Ray, Kevin Indig, Aleyda Solis weekly coverage)
How do you measure AI-content ROI in a world of LLM referral traffic decline? (Kevin Indig's data studies)
---
The Playbook (Coming Next)
Once research is synthesized, the playbook will cover:
Section 1: Production workflows
How to structure a content pipeline (prompt chaining, editing, QA layers)
Tools and techniques from practitioners (GPT agents, Claude Code, Clearscope, etc.)
Speed-to-publish benchmarks (Ahrefs: 6–12 min per draft; others: TBD)
Section 2: Guardrails
What Google flags as "scaled content abuse" (Lily Ray's research)
Penalty recovery case studies (e.g., Causal, sites hit by January 2026 listicle wave)
E-E-A-T requirements for AI content (where human editorship is non-negotiable)
Section 3: Where AI content wins / loses
Content types AI excels at (how-to, technical, reference, topical networks)
Content types AI struggles with (brand voice, original research, uniqueness)
Hybrid workflows (AI draft + human editing vs. 100% AI)
Section 4: Measurement
LLM referral traffic trends (decline from 2024 baseline; recovery opportunities)
AI Overviews impact on CTR and visibility
Tracking frameworks for AI-content performance
---
Data Collection Progress
[ ] Day 1: Scaffold repo, lock sources, create script templates
[ ] Day 2: Fetch YouTube transcripts (all 10 experts, 2–3 videos each)
[ ] Day 2: Fetch LinkedIn posts (all 10 experts, ~15 posts each)
[ ] Day 3: Synthesize patterns, write analysis, finalize README
---
Tools & Docs
YouTube Transcript API
Apify LinkedIn Post Scraper
Google's guidance on Scaled Content Abuse
Detailed.com SERP Research
iPullRank AI Search Manual
---
License
This research is for educational purposes. Expert content is cited and linked to original sources.
---
Last updated: June 2026  
Repo: https://github.com/justadityathing/ai-seo-content-research
