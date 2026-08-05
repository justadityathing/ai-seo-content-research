# AI-SEO Content Production: A Working Playbook

**Author:** Aditya ([justadityathing](https://github.com/justadityathing))
**Built from:** 16 YouTube transcripts, 60 LinkedIn posts, and reference articles from 10 practitioners — see [`/research`](./research)
**Scope:** Producing SEO content with AI at a scale between 10 and 200 pages per topic cluster, for a company that has something real to sell.
**Not in scope:** Pure affiliate churn, news publishing, and anything where the site itself is the product.

---

## How to read the citations in this document

Every recommendation below carries a source. Three honesty notes about what those sources can and cannot prove:

**1. LinkedIn posts have no permalinks.** The Apify `harvestapi/linkedin-profile-posts` actor returned an empty `URL` field for all 60 posts collected. I have the author, the exact post date, and the full text, but I cannot link to an individual post. LinkedIn citations below give the author's profile URL plus the post date. If you want to verify one, you'll have to scroll their activity feed to that date.

**2. One of my own sources is misdated, and I caught it late.** The file `research/youtube-transcripts/matt-diggity/2026-04--do-this-so-your-ai-content-doesnt-get-penalized.md` is labelled April 2026. The transcript references GPT models trained only to January 2022, the Will Smith/Chris Rock incident, Barbenheimer, and "dominate on Google in 2024." This is a 2023 video. My collection script took the date from the wrong metadata field. I have left the file in place and flagged it rather than quietly deleting it, because the error is instructive — it is exactly the kind of stale advice that gets recycled as current. See §6.

**3. Article citations are undated.** The reference articles in `research/other/key-articles.md` were collected by URL without publication dates. Where a date matters to the argument, I say so.

---

## Part 1 — The Pipeline

### Stage 1: Decide whether to use AI at all

**1.1 — Use AI for information-dense content. Keep humans on brand, opinion, and original research.**
This is the single strongest point of agreement across the dataset. Ryan Law and Mike King both report good results with AI-assisted how-to, technical, and reference content, while brand voice and original research still require people (source: Ryan Law, https://ahrefs.com/blog/my-complete-ai-content-process-for-ahrefs/, undated; Mike King, https://ipullrank.com/ai-search-manual, undated).

**1.2 — If your page exists only to restate what page one already says, don't build it.**
Cyrus Shepard's study of 400 sites that gained or lost Google traffic over 12 months found the winners were companies selling their own products, with manufacturers doing best and resellers a notch below. His framing: Google has a machine that makes infinite content now, so the durable position is content near task completion, not content that describes (source: Cyrus Shepard, https://www.youtube.com/watch?v=uz6D4do_r-c, 06.2026).

### Stage 2: Structure before volume

**2.1 — Build the topical map first, then generate into it.**
Koray Tuğberk Gübür's entire method treats topical coverage across a query network as the unit of work rather than the individual article, and he has published 48 custom GPT agents to automate map creation and semantic content production (source: Koray Tuğberk Gübür, https://medium.com/@ktgubur/korays-agents-generative-ai-agents-for-semantic-seo-and-topical-authority-d4b247fac72a, undated).

**2.2 — Target 20–50 substantial pieces per cluster, not 500 thin ones.**
Glen Allsopp's 250,000-keyword SERP analysis shows topic clusters dominating results (source: Glen Allsopp, https://detailed.com/state-of-content/, undated). The upper bound is set by penalty risk — see 4.2.

### Stage 3: Generation

**3.1 — Treat the pipeline as software, not as prompting.**
Ryan Law's Ahrefs system uses Claude Code with 23 custom skill files to produce publish-ready drafts in 6–12 minutes. The reason this matters is not the speed, it's that the pipeline is version-controlled and reproducible — a bad output is a bug you can fix once, rather than a prompt you rewrite forever (source: Ryan Law, https://ahrefs.com/blog/how-i-do-content-engineering-with-claude-code/, undated).

**3.2 — Ground every factual claim in a retrieved source, not in model memory.**
Hallucination is the failure mode that kills AI content on accuracy rather than on style. Retrieval-grounding is the standard fix. Note that I am recommending the principle here and explicitly rejecting the most-cited implementation of it — see §3, Rejection 1.

### Stage 4: Human review — the non-negotiable stage

**4.1 — Put named humans at fixed checkpoints, and make them accountable by name.**
Ryan Law's pipeline retains manual checkpoints even with heavy automation. No practitioner in this dataset advocates fully automated publishing (source: Ryan Law, https://ahrefs.com/blog/ai-content-wasnt-good-enough-now-it-is/, undated).

**4.2 — Assume a low-quality subfolder can sink the entire domain.**
This is the most actionable single finding in the research and it is not in most playbooks. Lily Ray's analysis of the January 2026 volatility found the AI-generated content was often isolated to one subfolder on an affected site, while the visibility drop hit the whole domain (source: Lily Ray, reported 08.06.2026, https://www.allineedformywebsite.com/expert-insights/lily-ray-ai-content-scaling-google-penalty/ — verification source, see note below). Practical consequence: you cannot ring-fence an AI content experiment in `/blog/ai/` and treat the risk as contained.

**4.3 — Do not publish self-promotional "best X" listicles at scale.**
Ray observed declines beginning around 20 January 2026 across dozens of sites; she has since spoken with roughly 20 affected companies and identified around 40 in her own research that had scaled self-promotional listicles, with one company having published 2,000 articles each claiming it was number one in its category (source: Lily Ray, https://www.buzzstream.com/blog/lily-ray-podcast/, 18.06.2026 — verification source). The tactic worked because it exploited a data void, and it stopped working because it scaled into a detectable footprint.

**4.4 — Remember that being cited is not being recommended.**
Ray analysed 100 B2B "best [category] software" queries in AI Overviews across three dates. Of the 80 that triggered an Overview, self-promotional listicles were cited 323 times — but in 224 of those cases Google cited the brand's own page while recommending a competitor instead (source: Lily Ray via Search Engine Land, https://searchengineland.com/google-ai-overviews-cite-self-serving-listicles-recommend-competitors-480573, 18.06.2026 — verification source). If your AI-visibility dashboard counts citations, it is measuring the wrong thing.

### Stage 5: Compliance

**5.1 — Read Google's scaled content abuse policy as an output test, not a method test.**
The policy applies to unoriginal, low-value content at scale regardless of whether a human, a machine, or both produced it. Using AI is not itself a violation (source: Google Search Central, https://developers.google.com/search/docs/essentials/spam-policies#scaled-content).

### Stage 6: Measurement

**6.1 — Instrument for AI surfaces separately from web results.**
Koray flagged Google Search Console's Generative AI performance reporting as the first real separation of AI impressions from traditional web-result impressions (source: Koray Tuğberk Gübür, https://tr.linkedin.com/in/koray-tugberk-gubur/, LinkedIn post 03.06.2026).

**6.2 — Watch "inauthentic mentions" as an emerging signal.**
Ray has said she is researching this as a possible Google signal for detecting manipulative content, with findings not yet published (source: Lily Ray, https://www.allineedformywebsite.com/expert-insights/lily-ray-ai-content-scaling-google-penalty/, 08.06.2026 — verification source). Flagged as a watch item, not a recommendation.

> **A note on verification sources.** Six citations above point outside my original ten-expert collection. My repo asserted a January 2026 penalty wave, but the Lily Ray transcript I collected (`2026-03--google-in-flux`) discusses the March 2024 core update and an August spam update — it does not actually support the January 2026 claim. Rather than cite my own synthesis for a claim its underlying transcript does not make, I went and verified it externally. The claim holds, and is now more precisely dated and better evidenced than it was in `patterns.md`.

---

## Part 2 — Where Experts Disagree

### Disagreement 1: Can AI content rank with no human editing?

- **Ryan Law and Matt Diggity:** No. Both build a mandatory human layer into their process (source: Ryan Law, https://ahrefs.com/blog/ai-content-wasnt-good-enough-now-it-is/, undated).
- **Koray Tuğberk Gübür:** Possibly yes, if semantic structure and topical authority are strong enough that the network carries the individual page (source: Koray Tuğberk Gübür, https://medium.com/@ktgubur/learn-advanced-true-seo-with-topical-authority-2-0-a985869b46bf, undated).
- **Lily Ray:** Irrelevant whether it can today, because Google corrects tactics once they scale into a detectable footprint (source: Lily Ray, https://www.buzzstream.com/blog/lily-ray-podcast/, 18.06.2026).

**My position: Ray, and not narrowly.** Law and Koray are arguing about whether unedited AI content *can* rank. Ray is making a different and better argument — that the question has a time dimension. Anything that works unusually well while being misaligned with how the system is supposed to work becomes a target precisely because it scales. Koray may well be empirically right that strong semantic structure carries weak pages today. That is an argument for doing it, not an argument for it being safe. The 4.2 finding decides it for me: if a bad subfolder can take down a whole domain, the expected value of skipping human review is negative regardless of whether it currently works.

### Disagreement 2: Is AEO a genuinely new discipline, or SEO on a new surface?

- **Eli Schwartz:** Different discipline — but note his position has moved. His article "AEO is not SEO 2.0" argues for difference in kind, while his June 2026 posts argue the AEO-replaces-SEO narrative failed because it was premised on Google losing, which did not happen (sources: https://www.productledseo.com/p/aeo-is-not-seo-20, undated; Eli Schwartz, https://www.linkedin.com/in/schwartze/, LinkedIn post 02.06.2026).
- **Kevin Indig:** Same tactics, different playing field, with a small genuine delta (source: Kevin Indig, https://www.youtube.com/watch?v=IhMVwbFsVBE, 01.2026 — panel discussion, see `research/youtube-transcripts/kevin-indig/2026-01--the-future-of-search-seo-ai-seo-aeo-geo.md`).
- **Lily Ray:** Roughly 90% overlap with SEO; the AEO framing distracts from E-E-A-T fundamentals (source: Lily Ray, stated in the same panel, 01.2026).

**My position: Indig and Ray on the substance, Schwartz on the staffing.** The 90% overlap figure matches what the rest of the dataset shows — the tactical work is recognisably SEO. But Schwartz makes a point the other two don't, which is that the *person* who does this well looks like a product manager rather than a technical specialist, and that companies hiring for AEO certifications are hiring the wrong profile (source: Eli Schwartz, LinkedIn post 11.06.2026). That is a real disagreement about org design hiding inside a semantic argument about naming. I think the discipline is 90% SEO and the ideal hire is 90% PM, and both can be true.

### Disagreement 3: Optimal publishing speed

- **Ryan Law:** Fast drafting, slow shipping — 6–12 minutes to a draft, then heavy editing (source: https://ahrefs.com/blog/how-i-do-content-engineering-with-claude-code/, undated).
- **Matt Diggity:** Faster cadence for affiliate and niche sites, one to two per day within topical clusters (source: Matt Diggity, https://www.youtube.com/watch?v=jOXQCCu2v3c, 12.2025).
- **Koray Tuğberk Gübür:** Depends on the topical authority phase; ramping a new map requires volume.

**My position: Law, with Koray's caveat, and I discount Diggity's entirely.** The three are not actually answering the same question, because they are running different businesses. Diggity's cadence is calibrated to affiliate sites, where the site is disposable and the downside of a penalty is losing an asset you were always willing to lose. If you are a SaaS company, your domain is not disposable. Speed advice does not transfer across risk profiles, and most people repeating Diggity's numbers have not noticed that they are importing his risk tolerance along with his cadence.

### Disagreement 4: Is the January 2026 listicle drop actually a Google action?

- **Lily Ray:** Yes — a targeted action against content-heavy sections, observed from around 20 January 2026 (source: https://ppc.land/lily-ray-what-the-seo-industry-is-getting-dangerously-wrong-about-ai-search/, 14.05.2026).
- **The counter-position, which nobody in my dataset states outright:** the January 2026 update was never confirmed by Google (source: Glenn Gabe, https://www.gsqi.com/marketing-blog/core-roars-back-google-may-2026-core-update-analysis/, 10.06.2026).

**My position: act on Ray's conclusion, but label it inference.** The pattern is strong — dozens of sites, one shared content type, correlated timing, and no recovery through the May 2026 core update. That is about as much evidence as the SEO industry ever gets. But it remains correlational analysis of an unconfirmed update, and the honest framing is "a tactic that stopped working around a date" rather than "a penalty Google issued." I include this disagreement because I had to construct one side of it myself, which tells you something about the dataset — see §5.

---

## Part 3 — What I Rejected and Why

### Rejection 1: Matt Diggity's "giga prompt" for factual accuracy

The method: point the model at the top-ranking pages for your target query, extract their facts, and write from those facts instead of from model memory. His stated logic is that if page one already has a fact wrong, it doesn't matter, because Google evidently doesn't care (source: Matt Diggity, https://www.youtube.com/watch?v=8ZFGmT0OqRY, misdated in my repo — actual date circa 2023).

**Why I rejected it.** The reasoning is self-defeating in two directions. First, a page synthesised entirely from page one is definitionally incapable of being better than page one — you have built a machine whose ceiling is parity, at exactly the moment Cyrus Shepard's 400-site study says parity content is what Google no longer needs. Second, "if page one is wrong it doesn't matter" is an argument that ranking and truth are the same thing. They are not, and building a factual accuracy process on that premise means your accuracy guarantee is only as good as your competitors' worst research. I keep the underlying principle — ground claims in retrieved sources — and reject this implementation of it. Retrieve from primary sources, not from the SERP.

### Rejection 2: Publishing volume as a route to topical authority

Koray's framework implies that establishing a topical map requires enough coverage to make the network legible, and that ramping phases need volume.

**Why I rejected it as a starting recommendation.** It is probably true and it is also the most dangerous true thing in the dataset for an inexperienced team to act on. It gives permission to publish a lot, and the failure mode of publishing a lot is the exact pattern Ray documented. Koray can run this safely because his semantic structure is genuinely sophisticated; a team reading a playbook cannot. I have capped the recommendation at 20–50 pieces per cluster (2.2) knowing this is more conservative than Koray would advise, and I would rather be wrong in the direction of under-publishing.

### Rejection 3: Optimising for AI citation counts

Several practitioners in the dataset treat AI Overview citations as the emerging success metric.

**Why I rejected it.** Ray's B2B analysis found 224 cases out of 323 citations where the brand was cited but a competitor was recommended (4.4). A metric that can move sharply in the right direction while the underlying business outcome moves in the wrong one is not a metric, it is a vanity number with a dashboard. Until someone publishes a citation-to-conversion study, I would not put this on a scorecard.

---

## Part 4 — My Original Ideas

### Idea 1: A cost-per-retained-page gate

**The gap.** Across 16 transcripts, 60 posts, and ten practitioners, I did not find a single unit-economics gate in any published pipeline. Everyone argues quality, penalty risk, and speed. Nobody publishes what a page costs them or what threshold kills a cluster.

**The idea.** Track cost per page that is still driving traffic 6 months post-publication — not cost per page published. A pipeline producing pages at ₹200 each with 20% survival is more expensive than one producing them at ₹600 with 90% survival, and the first pipeline is also the one accumulating the thin-content footprint that triggers the 4.2 domain-wide risk.

**Why it could work.** It converts the abstract "don't publish thin content" instruction into a number a finance team will enforce. Quality arguments lose to volume arguments in most companies because quality has no denominator. This gives it one. It also makes the penalty risk visible before the penalty, because survival rate degrades before visibility does.

**How to test it cheaply.** Tag every AI-assisted page at publication. At 6 months, pull the cohort and compute the share still receiving organic sessions. Two cohorts at different quality investments is enough to see whether the curve separates.

### Idea 2: Publish the methodology as the differentiator

**The gap.** The dataset treats disclosure as a compliance question — how much AI use must you admit to. Nobody treats it as a ranking asset.

**The idea.** For any comparison or "best of" content, publish the evaluation criteria, who tested what, and what was excluded, as a linked methodology page. Ray's analysis found the penalised listicles shared an absence of stated methodology, disclosed bias, or evidence of actual testing. If the absence of methodology is part of the detectable footprint, its presence is a cheap, structural differentiator that a content farm cannot fake at scale — because writing an honest methodology requires having actually done the work.

---

## Part 5 — Weaknesses of This Playbook

**The dataset is thin on the LinkedIn side.** I collected posts from 4 of 10 experts. Six profiles returned 404s from LinkedIn's unauthenticated API. My README frames this as deliberate channel weighting, and that framing is partly true and partly a rationalisation of a technical limitation I could not solve in the time available.

**Everything here is secondhand.** I have run no experiments. Every claim is a report by someone with a commercial interest in being seen as right — consultants selling consulting, tool builders selling tools, agencies selling audits. I have applied skepticism about incentives but I cannot substitute for primary data.

**Survivorship bias runs through the whole dataset.** These are ten practitioners who are visible because their approach appears to be working. I have no access to the people whose AI pipelines failed quietly.

**The penalty evidence is correlational.** As set out in Disagreement 4, the January 2026 event is an unconfirmed update. I am treating a pattern as a policy.

**My original ideas are untested.** Idea 1 requires a 6-month observation window I have not run. Idea 2 assumes methodology transparency is a durable signal rather than the next tactic to be gamed — which, by Ray's own logic about tactics that scale, it eventually will be.

**Recency.** The dataset was collected in June 2026 and the AI search surface is moving monthly. Sections 4 and 6 will decay fastest.

**One misdated source made it through my collection and into my analysis before I caught it.** If one date was wrong, others may be. I checked the remaining transcripts for internal date contradictions and found none, but I checked by keyword scan, not by watching 16 videos.

---

## Part 6 — Who I Would Not Recommend Following

### Matt Diggity

Three reasons, in ascending order of seriousness.

**1. The advice is stale but presented as current.** The video titled "Do THIS so your AI Content doesn't get PENALIZED" is built on GPT models trained to January 2022 and closes by pitching a masterclass on dominating Google in 2024. It surfaces today as evergreen guidance on AI penalties, in a field where the relevant Google actions happened in 2024, 2025, and 2026.

**2. Every piece of content is a funnel.** The 2025 strategy video pitches free agency audits in the opening 90 seconds; the AI content video pitches a masterclass mid-tutorial. This does not make him wrong. It does mean the incentive runs toward tactics that sound learnable and repeatable rather than toward tactics that are true, and it makes his experiment write-ups unverifiable — the sites are his, the data is his, and nothing is independently checkable.

**3. The risk profile is undisclosed and non-transferable.** This is the real problem. His methods are calibrated to affiliate portfolios where domains are expendable. He does not flag this, and readers import a risk tolerance they do not share along with the tactic. Given the finding that a single bad subfolder can drag down a whole domain (4.2), advice tuned for disposable sites is actively dangerous when applied to a company's primary domain.

**To be clear about what I am not saying:** I am not saying he is dishonest, and I included two of his videos in the research precisely because his experiments are a genuine data source. I would not recommend him to a junior marketer at a company with one domain and something to lose.

### A partial second: Koray Tuğberk Gübür

Not a "don't follow" — his framework is the most intellectually serious thing in the dataset, and 2.1 rests on it. But he is the one expert whose position on unedited AI content the other nine contradict, and his method is difficult to execute at his level of rigour. Someone following him without his semantic sophistication gets the volume and not the structure, which is precisely the failure pattern Ray documented. Follow him to learn how to think; do not follow him to get a checklist.

---

## Appendix: Source Index

Full annotated source list with channel selection rationale: [`research/sources.md`](./research/sources.md)
Cross-expert synthesis: [`patterns.md`](./patterns.md)
Collected transcripts: [`research/youtube-transcripts/`](./research/youtube-transcripts)
Collected LinkedIn posts: [`research/linkedin-posts/`](./research/linkedin-posts)
Google policy summary: [`research/other/google-scaled-content-policy.md`](./research/other/google-scaled-content-policy.md)

**Verification sources added during playbook writing** (outside the original ten-expert collection, used to check claims my own dataset asserted but did not evidence):

- Glenn Gabe, GSQi — https://www.gsqi.com/marketing-blog/core-roars-back-google-may-2026-core-update-analysis/ (10.06.2026)
- Search Engine Land on Lily Ray's AI Overviews analysis — https://searchengineland.com/google-ai-overviews-cite-self-serving-listicles-recommend-competitors-480573 (18.06.2026)
- PPC Land on Lily Ray — https://ppc.land/lily-ray-what-the-seo-industry-is-getting-dangerously-wrong-about-ai-search/ (14.05.2026)
- BuzzStream podcast with Lily Ray — https://www.buzzstream.com/blog/lily-ray-podcast/ (18.06.2026)
- All I Need For My Website on Lily Ray's June LinkedIn analysis — https://www.allineedformywebsite.com/expert-insights/lily-ray-ai-content-scaling-google-penalty/ (08.06.2026)
- Search Engine Roundtable on the January listicle updates — https://www.seroundtable.com/googleself-promotional-listicles-update-40873.html (04.02.2026)

---

*Last updated: August 2026*
