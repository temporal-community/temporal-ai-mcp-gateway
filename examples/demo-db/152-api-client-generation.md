---
Name: API Client Generation
Owner: Priya Raman
Status: In Review
Last Updated: 2026-03-28
---

## Problem

Client libraries for our public interface are written by hand in four languages. They lag the interface by between two weeks and two releases, they differ in ergonomics, and two of them are maintained by whoever last needed something from them.

## Proposal

Generate clients from the interface definition, with a thin hand-written layer for ergonomics.

- Generation from the specification on every interface change, as part of the release
- A hand-written layer per language for authentication, retries, and pagination helpers
- Version alignment with the interface, so a client version states what it supports
- Deprecation of hand-written clients on a published schedule

## Scope

The four current languages. Additional languages become cheap once this exists, which is part of the argument.

## Risks

Generated clients are idiomatic in no language unless the generator is configured carefully, and a library that feels foreign will be wrapped by its users, which puts us back where we started with more layers. The hand-written ergonomics layer is where this succeeds or fails and deserves real design attention per language.

## Measurement

Client lag behind interface releases, interface coverage per client, issues raised against clients, and adoption of generated versions.

## Dependencies

Generation is only as good as the specification, and ours is documentation rather than a contract. Three endpoints describe their response as an object with no schema, two use the same field name for different types across resources, and pagination style varies by resource. Those have to be fixed in the specification before a generator produces anything usable, and fixing them will surface places where the implementation and the document disagree.

- Specification validated in continuous integration, failing the build rather than warning
- Response schemas required on every endpoint before generation starts
- Pagination normalized in the specification, which may mean a visible interface change

## Migration

The two unmaintained clients are the easy case: generated versions replace them and nobody will notice. The two maintained ones have users who depend on hand-written conveniences the generator will not reproduce. Those conveniences are the specification for the ergonomics layer and need inventorying from the existing code before it is deprecated, not after.

## Prior Art

We generated server stubs from the same specification two years ago and abandoned the result. The reason is worth keeping: the generated code was fine and the specification was wrong, so every bug looked like a generator bug and nobody could tell the difference quickly. The specification work above is the lesson from that rather than an aside.
