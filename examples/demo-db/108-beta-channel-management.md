---
Name: Beta Channel Management
Owner: Ines Duarte
Status: In Review
Last Updated: 2026-04-11
---

## Context

Our beta channel has about nine hundred members, recruited over three years with no criteria and no way to leave other than uninstalling. Feedback comes through a shared mailbox and is read inconsistently. The channel's main function at present is early crash signal, which does not require nine hundred people.

## Proposal

Run the channel deliberately: defined cohorts, a feedback path, and a way out.

- Membership reviewed annually with an explicit renewal, which also prunes the inactive
- Cohorts by platform and device class so coverage is deliberate rather than accidental
- Feedback through an in-application path that carries build and context automatically
- A visible changelog for beta builds, because people testing deserve to know what changed

## Non-goals

No expansion of the channel. The current size is adequate and larger would not improve signal.

## Risks

Asking people to renew will shrink the channel, possibly sharply, and the shrunk channel may under-cover some device classes. Measuring coverage before and after is what tells us whether to recruit deliberately for the gaps.

## Measurement

Device class coverage, feedback items per release, crash signal lead time against general release, and renewal rate.

## Prior Art

The channel was assembled at conference booths, which explains its shape as well as its size: heavy on recent flagship hardware, nearly empty of the low-memory devices where most crashes happen. Research and design both run deliberate panels here, and both found a panel with a stated commitment and a way out produces more usable feedback at a third of the size. Neither keeps a changelog, and both report that the most common question from members is what changed.

## Staffing

Nine hundred members and a shared mailbox has meant no owner at all. The work is about a day a week: triaging in-application feedback, writing the beta changelog each release, and running the renewal once a year. The renewal is a two-week burst, since a renewal nobody chases is a silent cull of everyone who missed the message.

- Feedback triaged into the existing defect tracker rather than a separate list
- Changelog written from the release notes, not authored twice
- Coverage checked each quarter, so a gap is found before a release depends on it

## Failure Modes

The renewal is where this goes wrong quietly. Non-responders are removed, and the least likely to respond are the people who installed the build years ago and never looked again. That is the intended cull until it takes the only three members on an older device class with it. Coverage has to be read against the post-renewal roster before the next beta build ships, not after a crash goes unseen.
