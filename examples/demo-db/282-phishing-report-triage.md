---
Name: Phishing Report Triage
Owner: Jonas Keller
Status: Approved
Last Updated: 2026-04-22
---

## Context

Staff forward suspicious mail to a shared mailbox. Volume is about forty a week, the majority are marketing mail people find annoying rather than phishing, and the genuine ones sit in the same queue. Median time to a response is two days, which for a live credential-harvesting campaign is far too slow.

## Proposal

Automate the first pass and escalate the real ones quickly.

- A reporting control in the mail client rather than a forwarding address
- An AI classification pass that separates marketing nuisance from credible phishing, with the uncertain cases escalated rather than filed
- Automatic extraction of indicators and a check against threat intelligence for the credible set
- Confirmed campaigns triggering a search-and-purge across all mailboxes and a notice to staff

## Scope

Internal phishing reports. Customer reports of phishing impersonating us follow the abuse path.

## Risks

A classifier that files a real phish as nuisance is the whole risk, and the cost is asymmetric: a false negative is a potential compromise, a false positive is a person reading one more message. The classifier should escalate on any uncertainty, and a weekly sample of the auto-filed set must be reviewed by the security agents handling the queue to catch drift.

## Measurement

Time from report to assessment, credible phishing identified, false negatives found in the weekly sample, and reports per staff member, which should rise as reporting gets easier.

## Dependencies

Search-and-purge across all mailboxes needs an administrative permission on the mail platform that the security team does not hold today, and granting it makes purge available to everyone with that role. The permission belongs to a service identity that only the confirmed-campaign path can invoke, with every purge recorded, rather than being added to individual accounts.

## Staffing

Forty reports a week is roughly a day of someone's time, most of it spent on marketing mail. The automated first pass does not give that day back. It moves it into reviewing the weekly sample, confirming campaigns, and running purges, which is the work currently being crowded out. Nobody should plan headcount savings from this, and the rotation needs a second person through the first month while escalation thresholds settle.

## Failure Modes

The reporting control in the mail client can fail quietly. If a report never reaches the queue, the person who sent it believes they have discharged their responsibility and the message is never assessed, so the control has to confirm receipt to the reporter.

Rising volume is the expected outcome rather than a problem. Easier reporting means more nuisance reports, and handling those cheaply is the point.

## Open Questions

What the reporter hears back is undecided. Telling someone their report was filed as marketing mail teaches people what not to report, which is the opposite of what we want, and silence is what the current mailbox already does badly. The weekly review also has no defined action on finding a false negative beyond fixing that one message.
