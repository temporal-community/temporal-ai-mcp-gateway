---
Name: Localized Date and Number Input
Owner: Yusuf Demir
Status: Draft
Last Updated: 2025-11-05
---

## Background

Date entry assumes one order and number entry assumes one decimal separator. In several locales this means a date entered correctly is stored wrongly, and the error is silent because both readings are valid dates.

## Proposal

Use platform input affordances rather than parsing free text.

- Native date pickers everywhere a date is entered, with no text parsing path
- Numeric input using the locale's separator, with the parse driven by locale rather than by guess
- Stored values always canonical, with formatting applied only at display
- A migration review of existing records in the affected locales

## Scope

Input surfaces in the mobile applications. Imported data is a separate problem with its own ambiguity.

## Risks

The migration review is the uncomfortable part: we cannot distinguish a date that was entered wrongly from one that was entered correctly when both readings are valid. For ambiguous records the honest answer may be to ask the customer rather than to guess, which is operationally expensive.

## Measurement

Input errors reported per locale, corrections made to recently entered dates, and the count of ambiguous historical records, which tells us the size of the cleanup.

## Migration

The review can shrink the ambiguous set a long way before anyone contacts a customer. A date is unambiguous whenever its day component exceeds twelve, which resolves a large share outright, and more resolve against a neighbouring field: a start that falls after its end, a scheduled date already in the past when it was entered. What survives both passes is the population worth paying to ask about, and that number should be known before the contact process is designed rather than discovered during it.

## Interfaces Affected

- Every date field in the mobile applications, including the three that still accept typed text as a convenience for faster users
- Amount entry, where the locale separator decides what a trailing group of three digits means
- Display formatting, which has to read the same locale source as input or the two will drift apart
- Export, which writes the display format today and should write the canonical value

## Support Impact

Asking customers about ambiguous historical records is a campaign rather than a ticket queue: it needs a script, a way to record the answer against the record itself, and a rule for silence. Leaving an unanswered record untouched keeps a value we think is probably wrong; marking it visibly is honest and makes that customer's own reports look broken until they act. Neither is comfortable, and choosing between them is a decision for the owning team rather than for whoever writes the migration.
