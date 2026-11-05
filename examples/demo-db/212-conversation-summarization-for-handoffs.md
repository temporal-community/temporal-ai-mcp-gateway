---
Name: Conversation Summarization for Handoffs
Owner: Erin Vasquez
Status: In Review
Last Updated: 2026-07-17
---

## Problem

A ticket that passes between people loses context at every handoff. The receiving person reads the full thread, which for a long case is twenty messages, or skims it and asks the customer to repeat themselves. Customers cite being asked to repeat as their single largest frustration with our support.

## Proposal

Attach a maintained summary to every conversation, updated as it progresses.

- An AI summary covering the issue, what has been tried, and the current state, regenerated on each new message
- The summary editable by support agents, with edits preserved rather than overwritten
- Prominent placement above the thread, with the full thread one click away
- Summaries never shown to the customer, since they are an internal artifact

## Scope

Tickets and chat. Voice is out of scope until the voice pilot concludes.

## Risks

A summary that omits the thing that matters is worse than no summary, because the receiving person will trust it and skip the thread. The edit capability is what lets the previous handler correct it, and the interface should make reading the thread easy rather than making the summary feel sufficient. Commitments made to a customer are the most dangerous omission and should be extracted as a separate explicit field rather than left to prose.

## Measurement

Handoffs where the customer is asked to repeat information, time to first response after a handoff, and summary edit rate, which tells us how often it is wrong.

## Rollout

The commitments field ships before the prose summary. It is the part the risk above calls most dangerous, it is the easiest to score against a thread by hand, and a handler who trusts nothing else will still read a list of what we promised.

- Two weeks shadowed: summaries generated and stored, shown to nobody, scored against sampled threads by the queue leads
- Four weeks with one queue, chosen for long cases rather than high volume, since short tickets do not test a summary
- Wider rollout only once the edit rate has stopped falling, because a falling edit rate means the thing is still being corrected into shape

## Cost

Regenerating on every new message is the expensive choice and the right one, since a summary that lags the last message is the one somebody acts on. A twenty-message case regenerates twenty times, so cost scales with messages rather than with tickets. Holding the prior summary and passing only the new message keeps that affordable, and it also means a wrong summary carries forward until someone edits it, which is a reason to count the edit rate rather than assume quality.

## Open Questions

- Whether an edited summary is regenerated at all, or frozen until the handler releases it
- What the receiving person sees when generation fails: the previous summary with its age, or nothing
- Whether an extracted commitment is shown with the message it came from, which costs space but makes it checkable
- How long summaries are retained after a ticket closes, given they are internal and the thread is not
