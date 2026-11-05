---
Name: Permission Audit Export
Owner: Sofia Marchetti
Status: Approved
Last Updated: 2026-06-23
---

## Context

Enterprise customers are asked by their own auditors to produce a list of who has access to what. We have no export, so the account team assembles it from screenshots, which is slow, error-prone, and quietly embarrassing in a security review.

## Proposal

A self-serve export of effective permissions, generated on request and delivered as a signed file.

- Effective access per user, resolved through groups and templates rather than listed as raw grants
- A point-in-time snapshot with a generation timestamp, not a live view
- Change history for the preceding twelve months in a separate file
- An AI assistant in the admin console that answers plain questions about the export, such as who gained access to billing last quarter

## Scope

Organization-scoped exports for administrators. Individual users already see their own access in settings.

## Risks

The export is a complete map of who can reach what, which makes it a valuable document in the wrong hands. It must be delivered through an authenticated download rather than mailed, and generation should be logged as a sensitive action. The assistant answers from the generated snapshot only and must not reach into live permission data to fill gaps.

## Measurement

Exports generated per quarter, account team hours spent assembling access lists, and audit findings about access review, which is the reason customers ask.

## Dependencies

- A resolver that computes effective access exactly the way the enforcement path does, because two implementations will drift and the export is the one that gets audited
- Permission history at usable granularity; the audit log records the grant but not the resulting effective access, so twelve months of change history has to be reconstructed rather than read
- Authenticated download with its own expiry, which no artifact in the product has today
- A signing key and a documented way for a customer's auditor to verify it, which is what makes this file worth more than a spreadsheet

## Failure Modes

The export disagreeing with enforcement is the failure that matters. A customer shows an auditor a document saying someone cannot reach billing while the product lets them through, and the error now carries our signature. The guard is generating the export from the enforcement resolver rather than from a parallel implementation, plus a daily comparison on a sample of users that fails loudly. The assistant creates a second version of the same failure: an answer that paraphrases the snapshot loosely will be read as a statement about the system, so its answers need to cite the rows they came from.

## Timeline

The export is what customers actually asked for and should not wait behind anything else; it can be in administrators' hands well before the rest. Change history follows, and its schedule is set by the reconstruction work rather than by the file format. The assistant goes last, once the snapshot format has stopped moving, because every change to that format is a change to what it can truthfully say.
