---
Name: Penetration Test Cadence
Owner: Amara Osei
Status: In Review
Last Updated: 2026-05-31
---

## Context

We commission one external test a year, scoped to the main web application. Mobile has never been tested externally, nor has the public interface, and findings from the annual test are typically remediated shortly before the next one.

## Proposal

More frequent, narrower tests across a rotating scope, with remediation tracked properly.

- Quarterly tests with a rotating scope covering web, mobile, the public interface, and infrastructure
- Findings entering the normal engineering planning with severity-based deadlines
- Retest of high findings included in the engagement rather than deferred to next year
- An annual broader test retained for the compliance evidence

## Non-goals

No internal red team. That is a larger investment and should be considered separately once this baseline is in place.

## Risks

Quarterly testing produces findings faster than the current remediation capacity absorbs them, which will create a visible backlog. That backlog is real today and merely unmeasured, but making it visible without funding remediation would be a documentation exercise.

## Measurement

Scope coverage across a year, findings by severity, remediation within deadline, and repeat findings across engagements, which indicates remediation that did not hold.

## Cost

Four quarterly engagements plus the annual broad test is roughly twice the current external spend, and including retest of high findings adds about a fifth again. The larger cost is remediation, and the risk above is right that an unfunded backlog is only a documentation exercise, so engineering capacity has to be reserved each quarter before the test is booked rather than found afterwards.

- Two vendor relationships rather than one, so the rotation does not depend on a single firm's calendar
- The infrastructure quarter priced separately, since it needs a different skill set than the web quarters
- The annual test scoped to what compliance requires, not repeated across the quarterly scopes

## Staffing

Each engagement needs an internal owner for about two weeks: scoping, access provisioning, triage of the draft report, and the remediation handoff. Security can hold scoping and triage. The handoff has to reach the owning team, because a finding parked in a security backlog is a finding nobody with the context will fix.

## Timeline

The first quarter is web, repeating the current scope deliberately so the first comparison runs against something already measured. Mobile follows, since it has never been tested and is the likeliest source of high findings. The public interface and infrastructure take the back half of the year, and the annual broad test sits the quarter after infrastructure so its findings are not rediscovered weeks later.
