---
Name: Notebook Environment Standardization
Owner: Ines Duarte
Status: Draft
Last Updated: 2025-08-20
---

## Background

Analysts run notebooks on their own machines with their own library versions. Results are not reproducible across people, credentials live in local configuration files, and the environment setup for a new analyst takes most of a week.

## Proposal

A hosted notebook environment with a standard image and short-lived credentials.

- One base image per quarter, versioned, with a documented upgrade window
- Credentials issued at session start and expiring with the session
- Notebooks stored in version control rather than on the machine that ran them
- Compute sized per session with an idle timeout, because forgotten sessions are most of the cost

## Scope

Analysis notebooks. Model training has different hardware needs and is out of scope here.

## Risks

Hosted environments are slower to iterate in than a local machine, and analysts will notice immediately. If the gap is large the standard will be ignored, so the latency of the common loop matters more than any of the governance benefits in deciding whether this succeeds.

## Measurement

Share of analysis run in the hosted environment, setup time for a new analyst, and local credential files found during the next security review, which should be none.

## Cost

Per-session compute beats the laptops it replaces only if the idle timeout is short, and short timeouts are what makes hosting feel worse. Fifteen idle minutes with a warm restart is the compromise, which buys a pool sized to peak concurrency rather than to headcount.

- About twenty concurrent sessions at peak across forty analysts, which sizes the pool
- Notebook storage is trivial; cached datasets inside a session are not, and they do not survive a timeout
- The quarterly image build is half a day; the upgrade window costs more, since every pinned notebook is rechecked

## Migration

Notebooks move into version control before the environment switches, because a notebook that exists only on a laptop cannot run anywhere else and becomes the reason someone keeps the laptop workflow. The import is mechanical, and it reveals how many notebooks are genuinely in use, a number nobody has. Credentials are the forcing function: local configuration files stop working on an announced date, and that date moves the last holdouts rather than the governance argument.

## What Would Change Our Mind

The common loop decides this, and the common loop is a warehouse query followed by a plot. If the hosted round trip runs more than two seconds slower than local, analysts keep a local setup whatever the policy says, and the answer is to close the gap or drop the standard, not enforce it. If the gap is small and adoption still stalls, the image is missing what people need, which is a cadence problem rather than a hosting one.
