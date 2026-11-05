---
Name: Dependency Upgrade Automation
Owner: Nikhil Shah
Status: Shipped
Last Updated: 2025-07-30
---

## Background

Dependencies were upgraded when something forced it, usually a security advisory. The result was large, risky upgrades spanning many versions, performed under time pressure, which is the worst way to do it.

## Approach

Small, automatic, continuous upgrades with the test suite as the gate.

- Automated pull requests per dependency, grouped by ecosystem to limit volume
- Patch and minor versions merged automatically when the full suite passes
- Major versions raised as a change requiring a human, with the change notes attached
- A weekly digest of what merged and what is blocked, per team

## Non-goals

No automatic merging of major versions, and no automatic merging in the two repositories without adequate test coverage.

## Risks

Automatic merging trusts the test suite completely, which is only sound where coverage is good. We measured coverage per repository first and enabled automation only above a threshold, which excluded two repositories and made their coverage gap visible.

## Outcome

Shipped in June. Median dependency age fell from fourteen months to under two, and the last two security advisories required no action because we were already current.

## Cost

Continuous upgrades moved the cost from occasional large efforts to a constant background load on the build fleet. Grouping by ecosystem was the lever: ungrouped, the first week produced over four hundred pull requests and the queue times made everything else slower.

- Build minutes up about eighteen percent, concentrated in the overnight window where grouped runs land
- Review time down, since majors arrive one at a time with change notes rather than in a batch under advisory pressure
- The two excluded repositories still carry the old cost, now visible as a number rather than a feeling

## Operational Impact

An automatic merge is a change nobody read, which is fine until an incident starts with a dependency nobody remembers landing. The weekly digest is the record people reach for during an incident, so it carries merge times and not only versions.

## Failure Modes

A flaky test blocks a grouped upgrade and the group stays stuck, which looks exactly like nothing being released for that ecosystem; the digest's blocked list is where we find it, usually late. Worse is a flaky test that passes on retry and merges an upgrade the suite would otherwise have caught. Coverage above the threshold reduces that without removing it, which is the trade the risk above accepted. The third mode is a major pull request with no owner, which ages quietly while the digest counts it as blocked rather than ignored.
