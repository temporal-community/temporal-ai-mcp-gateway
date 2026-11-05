---
Name: Billing Address Validation
Owner: Victor Alves
Status: In Review
Last Updated: 2026-06-02
---

## Problem

We accept any string as a billing address. Bad addresses fail at three downstream points: tax jurisdiction resolution, card verification, and the physical mail finance occasionally has to send. Each failure surfaces days later as a separate ticket with no obvious common cause.

## Proposal

Validate at entry with the address provider we already use for shipping, and store the structured result alongside the raw input.

- Suggestions offered, never silently applied
- The raw string is always retained, because customers sometimes have good reasons
- Jurisdiction resolved from the structured form at save time, not at charge time
- An unvalidated address is allowed but flagged in the record

## Scope

The fifteen countries the provider covers well. Elsewhere the field stays free text with no validation theatre.

## Risks

Address validation fails most often for people whose addresses are already unusual, and the experience of being told your home does not exist is worse than the downstream ticket we are trying to prevent. Suggestions must be dismissible without friction and the flag must never block a purchase.

## Measurement

Tax jurisdiction mismatches per thousand invoices, card verification failures attributable to address, and the share of saves where a suggestion was offered and rejected, which tells us whether the provider is wrong about a region.

## Migration

Existing addresses are not revalidated in bulk. A backfill would flag a large number of accounts whose addresses work fine, and nothing downstream improves until an address is next used anyway. Validation happens on the next edit, so the flagged population grows slowly and stays interpretable.

- Jurisdiction stays as resolved at charge time for addresses never re-saved, so nothing moves under an untouched account
- A one-off read-only pass over the existing set to size the problem, writing nothing back
- An address in a covered country that fails validation on edit keeps its stored jurisdiction rather than losing it

## Interfaces Affected

- The billing address form, which gains the suggestion control and the dismiss path
- The invoice pipeline, which reads jurisdiction from the stored structured form instead of resolving per charge
- The provider client, called only from shipping today and now on the billing write path, which makes its latency a checkout concern
- Finance exports, which gain the structured fields and keep the raw string column

## What Would Change Our Mind

The rejected-suggestion rate decides this. If one region shows a high share of offered-and-rejected suggestions, the provider is wrong about that region and it leaves the covered fifteen rather than being argued with. If rejections are high everywhere, suggestion-at-entry is the wrong shape: validation belongs at save with a quiet flag and no prompt, which costs us the correction but keeps the data.
