---
Name: Security Training Refresh
Owner: Omar Haddad
Status: Draft
Last Updated: 2026-10-24
---

## Background

Annual security training is a video and a quiz, completed in about twenty minutes, mostly by clicking through. Completion is ninety-eight percent and it has no detectable effect on anything we measure, including phishing simulation results.

## Proposal

Replace the annual exercise with short, role-relevant, recurring content.

- Role-specific modules: engineers, support, finance, and everyone
- Five to ten minutes quarterly rather than twenty minutes annually
- Content tied to incidents and near-misses from our own history, anonymized
- Phishing simulation results feeding module selection for individuals, without punitive framing
- A module on AI generated phishing, which is the shape most of our recent near-misses have taken

## Non-goals

No change to the compliance evidence we need to produce, which the new format must still satisfy.

## Risks

Targeting modules based on simulation failure is one step from punishing people who fail, which produces hiding rather than learning. The framing and the data handling both need to be explicit: results used for content selection, never for performance.

## Measurement

Phishing simulation click and report rates, time to report a simulated phish, and whether reported real phishing attempts increase, which is the behavior we actually want.

## Data We Have

Three years of phishing simulation runs, plus the incident record the modules would draw on.

- Click and report rates per campaign, with role attached but not tenure
- Twenty-two near-misses and four incidents detailed enough to anonymize into a scenario
- Completion records for the annual exercise, which say who clicked through and nothing about what they learned

The gap is reporting speed. We recorded whether a simulated message was reported, not how long it took, so the first two quarters establish that number rather than move it.

## Timeline

Compliance evidence has to be continuous, so the annual exercise runs once more while the quarterly modules are built. Dropping it first leaves a hole in the audit record that costs more to explain than the twenty minutes costs to sit through. Engineer and finance modules come first, because that is where both the near-misses and the money are. Simulation-driven selection switches on a quarter later, after the framing has been written down and reviewed.

## Open Questions

Who may see individual simulation results. Selection needs them per person, and the moment a manager can read them the framing promised in the risks section is gone, so the access boundary has to be settled before the data is collected for this purpose. We have also not decided whether the quarterly module is mandatory in the compliance sense, which decides whether completion stays a ninety-eight percent number that means nothing.
