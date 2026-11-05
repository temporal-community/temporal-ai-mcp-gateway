---
Name: Invoice PDF Rendering Service
Owner: Grace Lindqvist
Status: Approved
Last Updated: 2026-03-30
---

## Background

Invoice PDFs are rendered inside the billing service by a library pinned six years ago. It cannot do right-to-left layout, it mangles several scripts, and it holds the request thread for up to four seconds on large invoices.

## Proposal

Extract rendering into its own service with a modern engine and an explicit template contract.

- Templates versioned and stored separately from code, with a preview environment
- Rendering requested asynchronously, with the document stored and linked rather than streamed
- Right-to-left and vertical layouts supported from day one
- Old invoices re-render against their original template version, never the current one

## Non-goals

No visual redesign. The layout stays as it is so that the migration is verifiable by diffing output.

## Risks

Pinning old invoices to old template versions is correct and also means carrying every template forever. The alternative, re-rendering history with the current template, changes documents that customers have filed for tax purposes, which we should not do.

## Success metrics

Render latency at the ninety-ninth percentile, billing service request time with rendering removed, and the count of scripts we can typeset correctly, which goes from eleven to the full supported set.

## Migration

Both renderers run against the same invoice set and the output is diffed before any customer receives a document from the new service. The no-redesign rule exists to make that diff meaningful, so any template change that is merely an improvement waits until the diff is clean. Comparing pixels will flag hinting differences no customer could see, so the comparison is on text runs and box positions, with the tolerance agreed before the run rather than negotiated after someone sees the failure count.

## Interfaces Affected

- The billing service drops its synchronous render call and carries a document reference on the invoice record instead
- Every caller expecting a PDF in the response body, which is the portal download and two internal tools
- Dunning mail, which attaches the invoice and now has to either wait on the stored document or send without it
- Template authoring, which leaves the billing repository and needs a review path of its own

## Cost

Storing every rendered document rather than generating on demand is the new recurring line, and at current invoice volume it is small enough that it should not drive the design. Carrying every template version forever costs almost nothing in storage and real effort in maintenance: each engine upgrade has to keep rendering templates written against the engine before it, and that obligation starts the day the first version is pinned.
