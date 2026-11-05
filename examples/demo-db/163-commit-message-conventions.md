---
Name: Commit Message Conventions
Owner: Lena Fischer
Status: Parked
Last Updated: 2025-09-26
---

## Background

Commit messages vary from a sentence to a word. A structured convention would enable automated change categorization, which the release notes work would benefit from, and would make history more searchable.

## Proposal

A lightweight convention with a type prefix and a scope, checked but not enforced strictly.

- Three types only: feature, fix, and chore, with a scope naming the area
- A check that warns rather than blocks, since blocking on message format at push time is hostile
- Existing history untouched
- Tooling consuming the convention where it adds value, rather than convention for its own sake

## Scope

The main repository, if it proceeds.

## Risks

Conventions that are checked but not enforced are followed by the people who would have written good messages anyway. Conventions that are enforced are satisfied minimally. Neither outcome clearly justifies the change, and the release notes work has since taken a different approach that does not depend on this.

Parked. The motivating use case went away and nobody has argued for it since on its own merits.

## Measurement

If it proceeds: convention adherence, and whether any tooling actually consumes it within a quarter.

## Prior Art

Two teams adopted a similar convention independently, one in the mobile repository and one in the data transformation repository, and both still use it. Neither built tooling on top. Asked why they keep it, both said the type prefix makes a scan of recent history faster, which is a real benefit and not one that needs a check or a proposal to obtain.

## Alternatives Considered

Deriving categories from pull request labels is what the release notes work now does, and it covers the motivating use case without touching commit messages. The remaining argument for a convention is searchable history, which labels do not help with, and nobody who actually searches history has made that argument. A template in the commit editor with no check at all was the lightest option considered: it costs nothing and would probably move the median message further than a warning does, since the people writing one-word messages are not reading warnings either.

## What Would Change Our Mind

A consumer. If something concrete needs a machine-readable type on a commit, a release process or a changelog or a bisect helper, and pull request labels genuinely cannot supply it, this comes back with that consumer named in the proposal. Without one, the honest position is that the convention is tidiness, and tidiness has not justified a repository-wide behavior change here before.
