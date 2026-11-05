---
Name: Receipt Localization
Owner: Felix Braun
Status: Shipped
Last Updated: 2025-06-16
---

## Background

Receipts are sent in English regardless of the account language, and the amount is formatted with a decimal point and a leading symbol in every locale. In three of our larger markets this makes receipts unusable for expense claims without manual retyping.

## Approach

Localize the receipt template and the number formatting, driven by the account's language and the charge currency.

- Template strings extracted and translated for the eleven supported languages
- Number and date formatting from the locale library rather than string concatenation
- Currency symbol placement and grouping per locale convention
- Legal footer text sourced per jurisdiction, reviewed once rather than per send

## Scope

Receipts only. Invoices have a separate template and a separate set of statutory requirements, and folding them together would have delayed both.

## Risks

The legal footer is the part that carries real exposure. Translating it without review in each jurisdiction would be worse than leaving it in English, so the footers shipped only for jurisdictions where review completed, and the rest fell back deliberately.

## Outcome

Shipped in April. Expense-claim tickets in the three affected markets fell by about seventy percent over the following two months, and two markets requested the same treatment for invoices, which is now queued.

## Review Notes

Legal review of the footers ran per jurisdiction and was the critical path, not the translation work. Six jurisdictions completed before the April release and the remainder fell back to English, which was the planned behaviour rather than a slip. The two markets now asking for the same treatment on invoices are both in the completed set, so their footer review carries over.

Two findings came out of the review worth recording. The locale library's currency formatting disagrees with local convention in one market on symbol spacing, and we followed the library rather than carry a per-market override. Grouping separators for the same language differ by country, so the format key had to be language and country rather than language alone, which was a change to the account language field's assumptions.

## Operational Impact

Eleven languages of template strings are now a standing translation obligation. A new receipt line means eleven translations before it can ship, and the April release set the expectation that receipts are not sent partly translated.

## Timeline

Extraction and formatting work took three weeks. Translation returned in two. Legal review ran eleven weeks across jurisdictions and determined the release date. The seventy percent fall in expense-claim tickets was measured over the two months after April, which is long enough to exclude the first-week spike and short enough that the invoice requests arrived before the measurement closed.
