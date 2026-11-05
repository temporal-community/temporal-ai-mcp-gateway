---
Name: Watch App Viability
Owner: Ruth Adeyemi
Status: Parked
Last Updated: 2025-12-22
---

## Context

We are asked about a watch application roughly once a quarter, usually by someone who has seen a competitor ship one. Nobody has established what it would be for beyond notification display, which the platform already provides without an application.

## Proposal

Establish whether there is a use case before building anything.

- Interviews with the twenty customers who have asked, about what they imagined
- A review of which of our interactions could complete in under ten seconds
- A prototype of the one or two candidates, if any survive the review
- An explicit decision to build or to decline, recorded either way

## Scope

Investigation only. No application development is proposed and none should start before the investigation concludes.

## Risks

The main risk is building it anyway because it is interesting, which is how most watch applications in our category appear to have been commissioned. The second risk is the maintenance tail: a watch application is a platform commitment, and declining later is harder than declining now.

## Measurement

Whether the investigation produces a use case that survives a prototype, and the decision recorded with its reasoning for the next time this is asked.

## Prior Art

Two competitors in our category shipped watch applications and one has since removed theirs. The survivor offers notification display and a single approval action. That is a data point about scope rather than about the decision: if the one that survived does one thing, the question is whether our equivalent of that one thing exists.

## Cost

The investigation is three weeks of one person, most of it interviews and the interaction review. That is cheap and is not the number that matters. A shipped watch application carries a platform SDK that changes annually, its own review on each release, and a build that breaks independently of the phone application. Two of our three mobile engineers have worked on one before and both put the ongoing cost at a day or two a month, indefinitely, for something that cannot be removed without a visible withdrawal.

## What Would Change Our Mind

One interaction that genuinely completes in under ten seconds and is done more than once a day would be enough to prototype. Approving a pending item is the obvious candidate and the only one anyone has named. If the interviews surface it and usage supports the frequency, this comes off the shelf. If twenty interviews produce twenty different answers, that is the decision, and it should be written down so the quarterly question has something to point at.
