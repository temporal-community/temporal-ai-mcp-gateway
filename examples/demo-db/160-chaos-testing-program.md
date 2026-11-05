---
Name: Chaos Testing Program
Owner: Maya Brennan
Status: Draft
Last Updated: 2025-10-26
---

## Background

We assume our retry logic, timeouts, and circuit breakers work. None of them is tested under the conditions they exist for. The evidence we do have is from real incidents, where several of them demonstrably did not work.

## Proposal

A small, deliberate program of fault injection in staging first, then production.

- Four fault types to start: instance loss, latency injection, dependency failure, and network partition
- Run against staging with production-like load until findings stop appearing
- Production experiments only with a defined blast radius and an abort mechanism
- Every finding tracked as a defect with an owner, which is the only output that matters

## Scope

Services on the shared platform with a defined owner. Unowned services are not candidates until they have one.

## Risks

Production fault injection causes real customer impact when the system responds worse than expected, which is precisely when the experiment is most valuable. The abort mechanism must be independent of the system being tested, and the appetite for this should be agreed by leadership before the first production run rather than negotiated after it.

## Measurement

Findings per experiment, findings resolved, and whether the next real incident of a tested class is handled better than the last one of the same class.

## Prior Art

The only fault injection exercise run here was a single instance-loss drill on the search service two years ago. It found three defects, two were fixed, and nobody ran another because the exercise had no owner and no cadence. That is the pattern this proposal has to avoid: findings without repetition produce a burst of fixes and a slow drift back to the same assumptions.

## Staffing

- A program owner who schedules experiments and chases findings, roughly a day a week
- The service's owning team present for each run, which is the expensive part and not optional, since an experiment nobody watches yields a report rather than a fix
- Someone independent holding the abort, never a participant in the experiment

Four fault types across the platform services is about a year at one experiment every two weeks, which is the honest pace. Going faster piles up unresolved findings, and unresolved findings turn the program into an audit nobody acts on.

## Open Questions

Staging with production-like load is asserted and is not true today: staging carries a fraction of the traffic and a different data shape. Whether to invest in making staging representative, or to accept staging findings as a weak signal and move to production sooner, is undecided, and that decision sets the whole timeline. The third defect from the search drill is also still open, which is a fact worth putting in front of whoever approves this.
