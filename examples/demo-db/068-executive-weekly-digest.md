---
Name: Executive Weekly Digest
Owner: Felix Braun
Status: In Review
Last Updated: 2026-05-11
---

## Problem

The weekly leadership pack is assembled by three analysts every Thursday, takes most of their day, and is largely mechanical: the same twelve charts, the same commentary structure, with real analysis only where something moved.

## Proposal

Generate the mechanical portion automatically and reserve human effort for the exceptions.

- Charts and tables generated from the semantic layer on a fixed schedule
- An AI drafting pass that writes the routine commentary and flags which metrics moved beyond their normal range
- Analysts review, correct, and write the analysis for flagged items only
- The draft clearly marked as such in the working copy, never in the circulated one

## Scope

The weekly pack. The quarterly review is a different artifact with a different audience and should stay hand-built.

## Risks

Routine commentary written by a model reads fluently whether or not it is right, and leadership will not be able to tell the difference. The review step is therefore mandatory and the analysts' names stay on the document, because accountability is what keeps the review real. We should also expect the draft to normalize whatever language it was trained on, including last quarter's framing of a problem that has since changed.

## Measurement

Analyst hours per pack, corrections made during review, and whether the flagged-metric list catches the things leadership asks about.

## Sequencing

Chart generation first, alone, for a month. That removes most of the mechanical Thursday and depends only on the semantic layer definitions being correct, which the month will test. The drafting pass comes second and only against a chart set already known to be right, because a fluent paragraph describing a wrong chart is far harder to catch than a wrong chart on its own.

- Month 1: charts and tables generated, analysts write all commentary as today
- Month 2: routine commentary drafted, analysts correct and record what they changed
- Month 3: out-of-range flagging evaluated against what leadership actually asked about

## Failure Modes

The review becomes a formality within about six weeks if the draft is usually acceptable, which is the normal outcome and the one that makes the accountability argument thin. Corrections per pack is the number to watch: a figure falling steadily toward zero means either the drafting improved or the reviewing stopped, and the two look identical from outside. The quieter failure is in the flagging, which derives each metric's normal range from its recent history, so a metric drifting badly for a quarter stops being flagged precisely because the drift has become its normal.

## Open Questions

Who is accountable when a circulated number is wrong is unsettled beyond leaving the analysts' names on the document. It is also unknown whether the working copy's draft marking survives a copy into a slide, which is how most of this material actually travels.
