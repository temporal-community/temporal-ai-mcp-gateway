---
Name: AI Readiness Survey Tooling
Owner: Nora Sellers
Status: Draft
Last Updated: 2025-11-14
---

## Background

The enterprise team runs a readiness questionnaire with prospective customers before a large deployment. It is a spreadsheet, filled in on a call, scored by hand, and the scoring rubric has three versions in circulation.

## Proposal

Move the questionnaire into a proper tool with one rubric and a record of every response.

- Questions and weights defined centrally, versioned, with the version recorded on each response
- Responses captured by the customer directly where they prefer, or by the team on a call
- Scoring computed rather than tallied, with the breakdown shown per section
- Completed assessments stored against the account so they are available at renewal

## Scope

The questionnaire and its scoring. The follow-on recommendations remain a human deliverable written by the solutions team.

## Risks

A score computed from a rubric looks more objective than it is, and a prospect shown a number will argue with the number rather than the underlying gaps. The breakdown by section matters more than the total, and the tool should make the total hard to quote in isolation.

## Measurement

Assessments completed per quarter, time from questionnaire to written recommendation, and the share of deployments where the assessment predicted the problems that actually occurred.

## Migration

The three rubrics in circulation have to be reconciled into one before anything gets built, and that is a solutions team decision rather than a tooling one. Past assessments are harder: roughly sixty completed spreadsheets exist, each scored against whichever rubric its author had. Rescoring them under the new weights would make them comparable and would also change numbers customers were already shown.

- One reconciled rubric agreed before the build starts
- Past spreadsheets imported as records, original rubric version noted, not rescored
- Anything older than two years left out, since the product it assessed no longer exists

## Interfaces Affected

Storing assessments against the account gives the account record a section account managers will read at renewal, which it has nowhere to put today. Customer-captured responses need an external path into the tool as well, and that path has to work for someone with no login here, which is a different authentication question from anything else the account record carries.

## Open Questions

Whether the customer sees their own total at all is undecided, and the concern about quoting a total in isolation cuts both ways. Withholding it keeps the conversation on the gaps, and it also makes the assessment feel like something done to them rather than with them.
