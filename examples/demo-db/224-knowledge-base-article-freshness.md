---
Name: Knowledge Base Article Freshness
Owner: Marcus Reyes
Status: In Review
Last Updated: 2026-03-10
---

## Problem

The help center has about nine hundred articles. Roughly a third describe behavior that has changed, and the only way an article gets corrected is if someone notices and files it. Customers following a stale article generate tickets that are our fault twice over.

## Proposal

Make staleness visible and tie article review to product change.

- Every article carrying a last-verified date, shown to readers
- Articles linked to the product areas they describe, so a release in that area flags them for review
- Low-traffic articles older than a year archived rather than reviewed, since the cost of keeping them exceeds their value
- A feedback control on every article routed to its owner, not to a general queue

## Scope

The public help center. Internal documentation has its own problem and its own proposal.

## Risks

Showing a last-verified date on a stale article tells the customer we know it is stale and left it there, which is worse than saying nothing unless the review actually happens. Committing to the display without the review capacity would be a mistake.

## Measurement

Articles verified within twelve months, tickets citing an article as the source of confusion, and article feedback volume by sentiment.

## Data We Have

Traffic per article goes back four years and decides the archive list. It is heavily skewed: the top sixty articles carry about seventy percent of reads, and roughly four hundred were read fewer than fifty times last year. Those four hundred are the archive candidates, which removes most of the work before any review starts.

- Ticket deflection per article, which shows which stale articles are actually costing us
- Last edit date on every article, which is not the same as last verified and must not be shown as if it were
- Release history by product area, which the review trigger needs and no article references today

## Staffing

Linking nine hundred articles to product areas is a one-time pass of about three weeks, and it needs someone who knows what each article describes. Ongoing review is the real commitment: with a third of the catalogue stale, the backlog is around three hundred articles, and clearing it inside a year means five or six reviews a week on top of the release-triggered ones.

## Sequencing

Archive first, link second, show the date last. Archiving the low-traffic four hundred shrinks the backlog before anyone commits to reviewing it. Linking to product areas gives the release trigger something to fire at. The last-verified date goes up only once the review loop is running, because a visible date on an unreviewed article is a published admission rather than a signal.
