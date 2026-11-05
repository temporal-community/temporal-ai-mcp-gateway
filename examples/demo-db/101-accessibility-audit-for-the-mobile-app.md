---
Name: Accessibility Audit for the Mobile App
Owner: Lena Fischer
Status: In Review
Last Updated: 2026-04-03
---

## Problem

We have never audited the mobile application against accessibility guidance. An external review of three screens found contrast failures, unlabeled controls, and a navigation order that makes the main list unusable with a screen reader. There is no reason to think the other screens are better.

## Proposal

Audit the full application, fix in priority order, and add automated checks to prevent regression.

- Full audit by an external specialist, screen by screen, with findings rated
- Blocking issues fixed before any new feature work on the affected screen
- Automated checks for labels and contrast in the build pipeline
- A manual screen reader pass added to the release checklist

## Scope

The mobile applications. The web product had its audit last year and has its own remediation plan.

## Risks

Automated checks catch perhaps a third of real issues and produce a green signal that invites complacency. The manual pass is the part that finds the navigation-order problems, and it is also the part most likely to be dropped when a release is late.

## Measurement

Findings closed by severity, automated check coverage, and completion of the manual pass per release, which should be reported rather than assumed.

## Prior Art

The web audit last year is the closest precedent, and its lesson is about remediation rather than the audit. Findings arrived as a single document of two hundred items that nobody could plan against, and rewriting it as tickets per screen took three weeks of someone's time. Findings delivered per screen, rated, in a form that imports as tickets is a contract term rather than a favor.

## Staffing

- An external specialist for the audit, roughly four weeks across both platforms
- Two engineers per platform on remediation, since the fixes are spread across the codebase rather than concentrated
- One named person owning the manual screen reader pass each release and reporting it, not a rotation

Remediation does not finish. Blocking issues gate feature work on the affected screen, which puts the cost in the planning of the teams that own those screens instead of in a central backlog nobody schedules.

## Timeline

The automated checks land before the audit finishes. They do not depend on the findings, and every week they are not running is another week of new unlabeled controls. The audit runs alongside. Remediation starts per screen as findings arrive rather than after the full report, which is the other lesson from the web audit, where waiting for the complete document cost a month.
