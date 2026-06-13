# LinkedIn Posts — Ryan Law
**Profile:** https://www.linkedin.com/in/ryanlaw/
**Posts fetched:** 0

---

## Access Limitation

This profile was targeted via the Apify `harvestapi/linkedin-profile-posts` actor (run 2026-06-13), but LinkedIn's API blocked unauthenticated access to the activity feed. The actor resolved the profile URL successfully but returned 0 posts — indicating the activity feed is restricted to authenticated (logged-in) users or the profile has limited public posting history.

A second actor (`supreme_coder/linkedin-post`) was also attempted with the same result.

**Workaround:** LinkedIn authentication (session cookies) would be required to access this profile's post history via Apify.

**Alternative data collected:** YouTube transcript content for Ryan Law is available in `research/youtube-transcripts/ryan-law/`.
