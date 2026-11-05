---
Name: Password Policy Simplification
Owner: Hugo Takahashi
Status: Shipped
Last Updated: 2025-07-29
---

## Problem

Our password rules required mixed case, a digit, a symbol, and ninety-day rotation. Every one of those requirements has been shown to produce worse passwords, and our own data agreed: predictable substitutions, incrementing digits at the end, and a spike in reset requests every quarter.

## Approach

Replace composition rules with length and a breach check.

- Minimum twelve characters, no composition requirements, no forced rotation
- Checked against a breached-credential corpus at set time and at sign-in
- Rotation required only on evidence of compromise
- Clear, specific feedback when a password is rejected, rather than a restated rule

## Scope

Individual passwords. Organization-level policy overrides stay available because some customers are contractually required to impose rules we think are wrong.

## Risks

The visible risk was customer perception: security teams read removal of complexity requirements as weakening. We prepared a short written rationale with references before launch and gave it to the account team, which turned out to be the most useful artifact of the project.

## Outcome

Shipped in June. Reset requests fell by about forty percent, breached-password rejections at set time run around two percent, and three enterprise customers have since relaxed their own overrides to match.

## Interfaces Affected

The breach check at sign-in is the part that reaches outside the password form. It runs on a successful authentication rather than before it, so a breached password still signs the person in and then requires a change. Blocking at that point would lock people out of their own accounts over a corpus we do not control. It is also the first external corpus the sign-in path consults, and it fails open: an unavailable corpus permits the sign-in and records that the check did not run.

## Support Impact

Rejection feedback was the detail that mattered most and was nearly cut. Telling someone their password appears in a known breach produces a different conversation than telling them it does not meet requirements, and the first almost never escalates where the second always did.

- Breach rejections carry their reason and a link to the written rationale
- Organization overrides are shown as the organization's rule, not ours
- Support can see when a check did not run, which matters while the corpus is unavailable

## Review Notes

The forty percent figure compares the quarter after launch against the quarter before, which contained a forced-rotation deadline. A full year will give the honest number and it will be smaller. Two percent is the more interesting result: one freely chosen password in fifty was already in a public corpus, which is the argument for the whole change.
