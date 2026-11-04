"""Activities that step the Monty sandbox one host-call at a time.

The core of the suspend-at-external-call design. Monty's *synchronous* stepping API
(``Monty(code).start()`` / ``snapshot.resume(...)``) runs the sandboxed script until it
calls a function the sandbox doesn't define — at which point it SUSPENDS and hands the
host a :class:`FunctionSnapshot` describing the pending call (name + args). The host does
the real work, then ``resume(...)`` continues from exactly that point.

Why this lives in Activities (not the Workflow):
  * Monty's *async* API (``acreate``/``run_async``) cannot run in a Temporal Workflow at
    all — its Rust↔asyncio bridge needs ``loop.call_soon_threadsafe``, which the
    deterministic Workflow loop forbids (it raises NotImplementedError). The synchronous
    ``start``/``resume`` API sidesteps that entirely — no event loop, no threads.
  * Even so, executing arbitrary (sandboxed) user code is not something to do inside a
    Workflow. So the Workflow stays the pure orchestrator: it calls ``monty_start`` once,
    then alternates the host-call Activity with ``monty_resume`` until the script completes.

The snapshot crosses the Activity boundary as bytes (``FunctionSnapshot.dump()`` /
``load_snapshot``). Those bytes can be large and end up in Workflow history.

No ``from __future__ import annotations`` — :class:`MontyStep` / :class:`MontyResumeInput`
cross Temporal's pydantic converter, and stringized annotations trip its TypeAdapter build.
"""

from typing import Any

import pydantic_monty as monty
from pydantic import BaseModel, ConfigDict, Field
from temporalio import activity
from temporalio.exceptions import ApplicationError

# Snapshot bytes are arbitrary binary (a serialized Monty continuation), so they are NOT
# valid UTF-8. Pydantic's default JSON encoding for ``bytes`` is UTF-8 and would fail
# ("invalid utf-8 sequence") — base64 encodes/decodes them losslessly on both legs.
_BYTES_AS_BASE64 = ConfigDict(ser_json_bytes="base64", val_json_bytes="base64")


class PendingCall(BaseModel):
    """One upstream tool call the script awaits: its Monty ``call_id`` plus the call itself.

    Every upstream tool is async (see the stub renderer), so when the script calls one Monty
    yields a FunctionSnapshot and the driver hands it a future (``{"future": ...}``) rather
    than blocking. These accumulate until the script awaits them (e.g. via ``asyncio.gather``),
    at which point the Workflow runs the batch — concurrently — and resumes with the results.
    """

    call_id: int
    function_name: str
    args: list[Any] = Field(default_factory=list)
    kwargs: dict[str, Any] = Field(default_factory=dict)


class MontyStep(BaseModel):
    """One step of a Monty run: either awaiting a batch of tool calls, or done.

    Returned by both :func:`monty_start` and :func:`monty_resume`. ``stdout``/``stderr`` are
    whatever the script printed *during this step* (the Workflow accumulates across steps).
    When ``done`` is False the script is suspended awaiting futures: ``calls`` lists every
    tool call *discovered* this step (call_id -> name/args/kwargs), ``pending_call_ids`` are
    the ones actually being awaited now, and ``snapshot`` carries the serialized continuation
    for :func:`monty_resume`. (The Workflow accumulates ``calls`` across steps so it can
    always resolve a ``pending_call_id`` even if the future was created in an earlier step.)
    When ``done`` is True, either ``output_json`` holds the script's final value or ``error``
    holds a script-level Monty error message (a bad script is data, not a Workflow failure).
    """

    model_config = _BYTES_AS_BASE64

    done: bool
    stdout: str = ""
    stderr: str = ""

    # Suspended-awaiting-futures fields (set when done is False).
    snapshot: bytes | None = None
    calls: list[PendingCall] = Field(default_factory=list)
    pending_call_ids: list[int] = Field(default_factory=list)

    # Terminal fields (set when done is True).
    output_json: str | None = None
    error: str | None = None


class MontyStartInput(BaseModel):
    """Input to :func:`monty_start`: the ``script`` to run plus the typed ``stubs`` it is type-checked against."""

    script: str
    stubs: str = ""


class CallResult(BaseModel):
    """The result of one awaited tool call, keyed by its Monty ``call_id``.

    Exactly one of a value (``return_value``) or an exception (``exc_type``/``message``) —
    the exception surfaces inside the sandbox at the matching ``await`` (catchable)."""

    call_id: int
    return_value: Any = None
    # Monty resume key is exc_type (NOT "exception_type"); must be a builtin exception name.
    exc_type: str | None = None
    message: str = ""


class MontyResumeInput(BaseModel):
    """Input to :func:`monty_resume`: the snapshot to continue plus a result per awaited call."""

    model_config = _BYTES_AS_BASE64

    snapshot: bytes
    results: list[CallResult] = Field(default_factory=list)


def _split_streams(streams: monty.CollectStreams) -> tuple[str, str]:
    """Join a :class:`CollectStreams` ``(stream, text)`` log into (stdout, stderr) strings."""
    out: list[str] = []
    err: list[str] = []
    for stream, text in streams.output:
        (out if stream == "stdout" else err).append(text)
    return "".join(out), "".join(err)


def _error_step(streams: monty.CollectStreams, e: monty.MontyError) -> MontyStep:
    stdout, stderr = _split_streams(streams)
    return MontyStep(done=True, stdout=stdout, stderr=stderr, error=f"{type(e).__name__}: {e}")


def _advance(snap: Any, streams: monty.CollectStreams) -> MontyStep:
    """Drive Monty forward from ``snap`` to the next batch of awaited tool calls (or the end).

    Every upstream tool is async, so each tool call surfaces as a FunctionSnapshot; we hand it
    a future (``{"future": ...}``) — which never blocks and does no real work — and keep
    stepping, recording each call, until the script actually awaits (a FutureSnapshot) or
    finishes. Handing back the whole FutureSnapshot batch lets the Workflow run those calls
    concurrently. A script error during any of these in-Activity resumes is data, not a
    failure, so it comes back as ``step.error``.
    """
    calls: list[PendingCall] = []
    while True:
        if isinstance(snap, monty.MontyComplete):
            stdout, stderr = _split_streams(streams)
            return MontyStep(
                done=True, stdout=stdout, stderr=stderr, output_json=snap.output_json()
            )
        if isinstance(snap, monty.FunctionSnapshot):
            calls.append(
                PendingCall(
                    call_id=snap.call_id,
                    function_name=snap.function_name,
                    args=list(snap.args),
                    kwargs=dict(snap.kwargs),
                )
            )
            try:
                snap = snap.resume({"future": ...})  # make it async; script gets a future
            except monty.MontyError as e:
                return _error_step(streams, e)
            continue
        if isinstance(snap, monty.FutureSnapshot):
            stdout, stderr = _split_streams(streams)
            return MontyStep(
                done=False,
                stdout=stdout,
                stderr=stderr,
                snapshot=snap.dump(),
                calls=calls,
                pending_call_ids=list(snap.pending_call_ids),
            )
        # NameLookupSnapshot (script referenced an unknown bare name) isn't supported by this
        # driver. Surface as a non-retryable failure rather than looping forever.
        raise ApplicationError(
            f"unsupported Monty suspension: {type(snap).__name__}",
            type="UnsupportedMontySuspension",
            non_retryable=True,
        )


@activity.defn
async def monty_start(input: MontyStartInput) -> MontyStep:
    """Type-check ``input.script`` against ``input.stubs``, then run it to the first host call (or completion).

    A bad script (syntax/type error) comes back as ``step.error``, not a Workflow failure."""
    activity.logger.info(
        "monty_start: compiling + starting (script_len=%d)", len(input.script)
    )
    streams = monty.CollectStreams()
    try:
        snap = monty.Monty(
            input.script, type_check=True, type_check_stubs=input.stubs
        ).start(print_callback=streams)
    except monty.MontyError as e:
        activity.logger.warning("monty_start: %s: %s", type(e).__name__, e)
        return _error_step(streams, e)
    step = _advance(snap, streams)
    activity.logger.info(
        "monty_start: %s",
        "done" if step.done else f"awaiting {len(step.pending_call_ids)} call(s)",
    )
    return step


def _result_value(r: CallResult) -> dict:
    """One CallResult -> Monty's ExternalResult dict (return value or exception-by-name)."""
    if r.exc_type is not None:
        return {"exc_type": r.exc_type, "message": r.message}
    return {"return_value": r.return_value}


@activity.defn
async def monty_resume(input: MontyResumeInput) -> MontyStep:
    """Resume a FutureSnapshot with a result per awaited call, then advance to the next batch."""
    streams = monty.CollectStreams()
    snap = monty.load_snapshot(input.snapshot, print_callback=streams)
    if not isinstance(snap, monty.FutureSnapshot):
        # The driver only ever dumps FutureSnapshots; anything else is a programming error.
        raise ApplicationError(
            f"monty_resume expected a FutureSnapshot, got {type(snap).__name__}",
            type="MontyUnexpectedSnapshot",
            non_retryable=True,
        )
    results = {r.call_id: _result_value(r) for r in input.results}
    try:
        resumed = snap.resume(results)
    except monty.MontyError as e:
        activity.logger.warning("monty_resume: %s: %s", type(e).__name__, e)
        return _error_step(streams, e)
    step = _advance(resumed, streams)
    activity.logger.info(
        "monty_resume: %s",
        "done" if step.done else f"awaiting {len(step.pending_call_ids)} call(s)",
    )
    return step
