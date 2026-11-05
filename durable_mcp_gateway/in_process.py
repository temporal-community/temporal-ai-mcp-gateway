"""Run scripts in this process, without Temporal: the runner behind ``--no-temporal``.

The same start → gather pending tool calls → resume loop as :class:`RunScriptWorkflow`, calling
the same Activity functions directly (``@activity.defn`` returns the plain function), so a
script behaves the same in both modes and gets the same reply. What is missing is durability:
each tool call is tried once, and nothing outlives the process, so a process exit loses every
run in flight.
"""

from __future__ import annotations

import asyncio
import itertools
import json
import time
from collections.abc import Callable, Iterator
from uuid import uuid4

from . import activities, config
from .models import CallToolRequest, CallToolResult
from .monty_activities import (
    CallResult,
    MontyResumeInput,
    MontyStartInput,
    PendingCall,
    monty_resume,
    monty_start,
)
from .workflow import _format_reply


class InProcessRunner:
    """Runs scripts in this process, at most ``config.MAX_CONCURRENT_ACTIVITIES`` tool calls at
    a time across every run (the backend Worker's cap). ``progress``, if given, receives one
    line per finished tool call."""

    def __init__(self, progress: Callable[[str], None] | None = None) -> None:
        self._call_slots = asyncio.Semaphore(config.MAX_CONCURRENT_ACTIVITIES)
        self._progress = progress

    async def run_script(self, script: str, session_id: str) -> str:
        """Run ``script`` to completion and return the reply :class:`RunScriptWorkflow` would.

        A tool failure, including one the Workflow would have retried, reaches the script as a
        catchable RuntimeError at its await.
        """
        run_id = uuid4().hex[:8]
        finished = itertools.count(1)
        stubs = await activities.get_catalog_stub()
        step = await monty_start(MontyStartInput(script=script, stubs=stubs))
        stdout_parts = [step.stdout]
        stderr_parts = [step.stderr]
        call_meta: dict[int, PendingCall] = {}
        while not step.done:
            for c in step.calls:
                call_meta[c.call_id] = c
            results = await asyncio.gather(
                *[
                    self._call_tool(run_id, finished, call_meta[cid], session_id)
                    for cid in step.pending_call_ids
                ]
            )
            step = await monty_resume(
                MontyResumeInput(snapshot=step.snapshot, results=list(results))
            )
            stdout_parts.append(step.stdout)
            stderr_parts.append(step.stderr)

        if step.error:
            return f"Script error ({step.error})"
        output = json.loads(step.output_json) if step.output_json else None
        stdout = "".join(stdout_parts).strip()
        stderr = "".join(stderr_parts).strip()
        return _format_reply(stdout, stderr, repr(output))

    async def _call_tool(
        self, run_id: str, finished: Iterator[int], call: PendingCall, session_id: str
    ) -> CallResult:
        request = CallToolRequest(
            name=call.function_name, arguments=call.kwargs, session_id=session_id
        )
        async with self._call_slots:
            started = time.monotonic()
            try:
                result = await activities.call_tool_activity(request)
            except Exception as e:  # noqa: BLE001 - no retries here; the script gets the failure
                result = CallToolResult(ok=False, error=f"tool call failed: {e}")
            secs = time.monotonic() - started
        if self._progress is not None:
            status = "ok" if result.ok else f"FAILED: {result.error}".replace("\n", " ")[:120]
            self._progress(
                f"run {run_id} #{next(finished):<4} {call.function_name:<28} {secs:6.2f}s  {status}"
            )
        if result.ok:
            return CallResult(call_id=call.call_id, return_value=result.result)
        return CallResult(
            call_id=call.call_id,
            exc_type="RuntimeError",
            message=result.error or "tool failed",
        )
