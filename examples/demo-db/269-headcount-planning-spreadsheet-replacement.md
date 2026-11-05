---
Name: Headcount Planning Spreadsheet Replacement
Owner: Amara Osei
Status: Parked
Last Updated: 2026-01-10
---

## Background

Headcount planning runs in a spreadsheet with one tab per department, consolidated by hand each quarter. It breaks in predictable ways: stale copies, formula errors in the consolidation, and no history of what was approved when.

## Proposal

A purpose-built planning model with approval state and history.

- Positions as records with state: planned, approved, open, filled, or cancelled
- Approval recorded with date and approver, giving an auditable history
- Consolidation computed rather than assembled
- Integration with the recruiting system so open positions reconcile automatically

## Scope

Headcount planning and approval. Compensation planning is separate and more sensitive.

## Risks

This is a buy rather than build decision and we have not evaluated the market. Building it would be straightforward and would commit us to maintaining a finance tool, which is not where our engineering capacity should go.

Parked pending a vendor evaluation, which finance has agreed to run.

## Measurement

If it proceeds: time to consolidate a quarterly plan, discrepancies between the plan and the recruiting system, and approval history completeness.

## Alternatives Considered

Hardening the spreadsheet is the cheapest thing on the list: one source file, a locked consolidation tab, a named owner per department. It removes the stale copies and the formula errors and does nothing about approval history, which is the part that gets asked for after the fact and cannot be reconstructed. A workflow tool holding only the approvals, with planning left in the spreadsheet, splits the data across two places and leaves the consolidation manual.

## Cost

The build estimate is small and the maintenance is the real number. A finance tool collects requests every planning cycle: a new position state, another consolidation view, a field for the reorganization nobody planned for. Vendor pricing in this category tends to be per employee per year, so the cost grows with the thing being planned. That comparison is what the evaluation has to produce, rather than a feature grid.

## What Would Change Our Mind

If the evaluation finds nothing that reconciles with our recruiting system, that bullet becomes the deciding one and building returns to the table, since reconciliation by hand is most of the present pain. The other case is scope. If compensation planning is folded in later, the sensitivity changes the access model enough that this is no longer the same project, and the parked decision should be reopened rather than resumed.
