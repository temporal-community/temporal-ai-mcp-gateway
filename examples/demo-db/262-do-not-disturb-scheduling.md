---
Name: Do Not Disturb Scheduling
Owner: Grace Lindqvist
Status: Shipped
Last Updated: 2025-07-04
---

## Context

Notifications arrived at all hours. For a product used across time zones, this meant people in one region receiving pushes overnight from colleagues working normally elsewhere, and the only remedy was turning notifications off entirely.

## Approach

Scheduled quiet hours with sensible defaults and an override for genuine urgency.

- Quiet hours defaulted from the person's own time zone and working hours
- Notifications held and delivered at the end of quiet hours rather than dropped
- A marked-urgent path that breaks through, available but deliberately not prominent
- The sender shown that the recipient is in quiet hours before sending

## Non-goals

No automatic inference of working hours from activity, which would be both creepy and frequently wrong.

## Risks

The breakthrough path is the part that could be abused into meaninglessness, which is what happens to every urgent flag given enough time. Keeping it a separate deliberate action rather than a checkbox on the compose form has kept usage low so far.

## Outcome

Shipped in June. About a third of people have quiet hours configured, overnight push volume is down substantially in the affected regions, and the breakthrough path is used on well under one percent of messages.

## Operational Impact

Holding notifications rather than dropping them moved push traffic into a spike at the end of each quiet window, and in the largest region that spike is now the daily peak for the delivery service. Capacity was sized for it before launch; the jitter added to release times spreads it over fifteen minutes, which costs a small delay against a peak the service would otherwise have to carry.

A held notification whose underlying message is deleted before release is discarded rather than delivered, so a person waking up does not receive a push for something that no longer exists.

## Support Impact

- Two question types dominate: why a message was not received, and how to turn quiet hours off for a day
- Both are answered from the sender-side quiet-hours indicator, which support can see
- Breakthrough usage is visible per sender, which has been enough to handle the two reports of overuse without a policy

## Prior Art

The marked-urgent path was built after watching how the same mechanism decays elsewhere: a flag attached to the compose form becomes default-on within a quarter. Keeping it a separate action, two steps away and with the recipient's local time shown at the point of use, is the whole reason breakthrough usage has stayed under one percent. The cost is that genuinely urgent messages take longer to send, which is a cost the design accepted.
