---
Name: Release Notes Automation
Owner: Grace Lindqvist
Status: In Review
Last Updated: 2026-03-02
---

## Problem

Customer-facing release notes are written by a product manager reading a list of merged changes, most of which are internal and irrelevant. It takes a few hours per release and the result is inconsistent in both coverage and tone.

## Proposal

Generate a draft from structured change metadata, written at the time of the change.

- A required customer-impact field on changes that touch customer-visible behavior
- A draft assembled per release from those fields, grouped by area
- The product manager editing and publishing rather than compiling
- Changes without the field excluded from the draft and listed separately for review

## Non-goals

No generation of the impact description itself. The person who made the change is best placed to say what it does for a customer, and asking them at the time is the whole point.

## Risks

A required field on changes is a tax paid by every engineer for a document most of them will never read, and the predictable response is a field filled in with the commit message. The field should be optional with a prompt rather than mandatory with a default, and the separate list of excluded changes is what catches omissions.

## Measurement

Time to publish release notes, share of customer-visible changes with a usable impact description, and edits required to the draft before publishing.

## Interfaces Affected

The change workflow is where the cost lands, so the prompt has to appear where the engineer already is rather than in a separate tool. Area grouping needs a mapping from code ownership to the customer-facing areas the notes use, which are different taxonomies with no translation between them today. The draft arrives in the publishing tool as a document the product manager edits, not as a message to copy out of, since copying is how inconsistent tone survives automation.

## Rollout

One team's changes first, with their drafts produced alongside the hand-written notes for two releases. That comparison is the only way to see whether the impact descriptions are usable, and usable is the measure rather than present. The excluded list is read in both releases, because the first thing it shows is how many customer-visible changes the prompt is missing, which decides whether the prompt sits in the right place.

## What Would Change Our Mind

If editing the draft stays as expensive as writing from scratch, the field is producing text nobody can publish, and the prompt is the problem rather than the pipeline. If the excluded list is reliably long and reliably full of real customer impact, the optional field is being skipped by default and the compromise in the risks section has failed, which argues for a check at release time instead of a tax at change time.
