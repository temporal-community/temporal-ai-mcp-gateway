---
Name: Security Questionnaire Automation
Owner: Yusuf Demir
Status: Draft
Last Updated: 2025-08-07
---

## Problem

Enterprise prospects send security questionnaires, typically two hundred questions, and each takes a security engineer most of a day. We receive about four a month and the answers are substantially the same each time, reassembled by hand from previous responses.

## Proposal

A maintained answer library with a review step, rather than reassembly from memory.

- A canonical answer per question topic, owned and dated
- Matching incoming questions to library topics, with the match reviewed rather than trusted
- Answers marked stale when the underlying control changes, through a link to the control owner
- Completed questionnaires retained, so the same customer's annual reassessment is cheap

## Non-goals

No automatic submission. A security questionnaire is a contractual representation and a person signs it.

## Risks

A library makes it easy to give an answer that was true when written and is not now. The link between an answer and the control it describes is the mechanism that prevents this, and it only works if control owners actually mark changes, which is the part that will decay.

## Measurement

Engineer hours per questionnaire, library coverage of incoming questions, stale answers caught at review, and turnaround time to the prospect.

## Dependencies

The staleness mechanism needs a control register that records when each control last changed. We have a register for audit purposes; it lists controls and owners and records nothing between annual reviews. Linking answers to it today would link them to something that updates once a year, which is slower than the questionnaires arrive.

- Control register extended with a change date and a change note
- Answer-to-control links are many-to-many; one answer often describes three controls
- Library ownership sits with the security team, not with whoever wrote an answer first

## Failure Modes

The dangerous case is a confident wrong answer, and the review step is the only thing standing between the library and one. A reviewer reading two hundred matched answers will be skimming by question one hundred, so the review has to surface what changed since the last questionnaire rather than presenting all two hundred equally.

## Timeline

Four questionnaires a month means the library builds from real traffic rather than an upfront writing exercise. The first three months produce coverage of the common questions at no cost beyond the engineer's existing day. Matching and the review surface come after there is enough library to match against; building them first leaves a matcher with nothing on the other side.
