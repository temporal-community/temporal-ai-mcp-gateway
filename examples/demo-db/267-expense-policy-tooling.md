---
Name: Expense Policy Tooling
Owner: Hana Kobayashi
Status: Draft
Last Updated: 2026-05-18
---

## Problem

The expense policy is a document and the expense tool knows nothing about it. People submit claims that breach policy without realizing, finance rejects them weeks later, and the resulting exchange is unpleasant for everyone and slow.

## Proposal

Encode the checkable parts of the policy into the submission flow.

- Category limits and receipt requirements checked at submission with a specific message
- Pre-approval prompted at the point of a known threshold rather than discovered afterwards
- Policy text linked from each check, so the rule is visible rather than asserted
- Exceptions requestable in the flow, with approval routed rather than emailed

## Scope

The checkable rules. Judgment-based rules such as reasonableness stay with the approver.

## Risks

Encoding a policy exposes its inconsistencies, and this policy has several, including two category limits that contradict the travel section. Those need resolving before encoding, which is a finance decision and a prerequisite rather than a side effect.

## Measurement

Claims rejected after submission, time from submission to reimbursement, exceptions requested, and policy questions to finance.

## Rollout

The contradicting limits are resolved first, since encoding them is impossible and the rest waits behind that decision. The checks then run as warnings rather than blocks for one monthly cycle, so finance can see what share of real claims each rule would stop before anyone is prevented from submitting. A rule that fires on half of all meal claims is a policy problem surfacing, not a tooling success.

- Finance resolves the travel section conflicts
- Checks run as warnings for one cycle, fire rate recorded per rule
- Blocking enabled rule by rule, starting with receipt requirements

## Interfaces Affected

Submission gains a validation step that the mobile path cannot run at capture time, because it uploads a photograph first and collects category and amount later. Exception routing needs an approver list the expense tool does not hold: it uses the reporting line from the directory, which is right for ordinary approvals and wrong for exceptions that belong to finance.

## Open Questions

Whether a blocked claim can be overridden by the claimant with a stated reason, or only through the exception path, is undecided. So is the handling of claims submitted against a policy version that has since changed, which is routine for anything filed late. The fair rule is the policy in force on the expense date, and the tool has no concept of a policy version.
