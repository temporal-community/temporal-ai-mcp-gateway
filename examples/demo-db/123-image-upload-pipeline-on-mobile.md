---
Name: Image Upload Pipeline on Mobile
Owner: Marcus Reyes
Status: Draft
Last Updated: 2025-12-01
---

## Problem

Images upload at full resolution over whatever connection is available. On cellular this is slow, expensive for the customer, and fails often enough that the retry path is the common path rather than the exception.

## Proposal

Resize and queue on the device, with upload managed as a background task.

- Resize to the largest size any surface actually displays, before upload
- A persistent queue surviving application restart, with per-item state
- Upload deferred to an unmetered connection by default, with an override
- Original retained locally until the upload confirms, then released

## Scope

Images. Documents and video have different constraints and are explicitly out of scope.

## Risks

Resizing on device discards information permanently, and we have no way to know today whether any customer needs the original resolution for something we have not thought of. Keeping the original until confirmation does not help here; once uploaded, the resized version is what exists. This needs a decision rather than a default.

## Measurement

Upload success rate by connection type, time to visible, data transferred per upload, and complaints about image quality, which is the signal that the resize target is wrong.

## Data We Have

The largest surface that renders an uploaded image is the listing detail view at twice the widest supported device width, and that is where the resize target comes from, not a round number. Upload telemetry gives the rest.

- Failure rate by connection type, four times higher on cellular than on unmetered connections
- Bytes per upload, where the median image is about eight times the largest displayed size
- Retry counts per upload, which is how we know retrying is the common path

## Alternatives Considered

Uploading the original and resizing server-side keeps every pixel and fixes nothing: the cost is transfer, not storage. Sending a small version immediately and the full one later was more interesting, because the image appears fast and the original survives. It was set aside because two versions means two states to reconcile, and the queue has to survive restart either way, which doubles the hard part.

## Failure Modes

The restart-safe queue is where this goes subtly wrong. An item marked uploading when the application was killed is either uploaded or not, and the device cannot tell without asking the server, so the state machine needs an explicit unknown that resolves by querying rather than by retrying blindly. Blind retry here means duplicate images. Deferring to unmetered has its own version: a listing created on cellular and never reopened on an unmetered connection keeps no images at all while the seller believes it is published, so the queue needs an age at which it asks rather than waits.
