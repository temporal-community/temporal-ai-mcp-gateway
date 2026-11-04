"""The Workflow that durably runs a sandboxed Python script.

One Workflow runs a user-supplied script (see :class:`RunScript`) inside the pydantic-monty
sandbox, calling upstream tools as ordinary Python functions. The Workflow is a pure
orchestrator — it never runs Monty itself; it threads opaque snapshot bytes between the
stepping Activities.
"""

from __future__ import annotations

import asyncio
import json
from datetime import timedelta

from temporalio import workflow
from temporalio.common import RetryPolicy
from temporalio.exceptions import ActivityError

# NOTE: pydantic_monty is intentionally NOT imported here. The Monty interpreter never
# runs in the Workflow — it runs in the monty_start/monty_resume Activities. The Workflow
# is a pure orchestrator that threads opaque snapshot bytes between those Activities.
with workflow.unsafe.imports_passed_through():
    from . import activities
    from .models import CallToolRequest, Catalog, RunScript
    from .monty_activities import (
        CallResult,
        MontyResumeInput,
        MontyStartInput,
        MontyStep,
        PendingCall,
        monty_resume,
        monty_start,
    )


# Ceiling for a single Monty step (compile+run-to-first-call, or resume-to-next-call).
# Sandboxed compute between host calls should be fast; a generous bound still bounds runaway.
_MONTY_STEP_TIMEOUT = timedelta(seconds=30)

# Ceiling for one host/data Activity (tool call, catalog fetch).
_ACTIVITY_TIMEOUT = timedelta(minutes=10)

# Retry policy for upstream tool calls: only RetryableUpstreamError (rate limit / 5xx /
# dropped connection) is ever raised from call_tool_activity, so this rides through an
# intermittently-throttling upstream (e.g. Notion's 429s) with backoff. Bounded so a truly
# dead endpoint gives up instead of retrying forever; on exhaustion the workflow turns the
# failure into a catchable script error (see _dispatch_one).
_TOOL_RETRY = RetryPolicy(
    initial_interval=timedelta(seconds=1),
    backoff_coefficient=2.0,
    maximum_interval=timedelta(seconds=30),
    maximum_attempts=8,
)


def _call_summary(call: PendingCall) -> str:
    """The Activity's summary in the Temporal UI timeline — the upstream tool's function name,
    instead of the generic ``call_tool_activity``. Just the name: arg hints ate too much
    horizontal space in the timeline rows."""
    return call.function_name


def _format_reply(stdout: str, stderr: str, output_repr: str) -> str:
    """Assemble the script reply: ``output:``/``stderr:`` blocks (each omitted when empty)
    followed by the ``result:`` line."""
    parts: list[str] = []
    if stdout:
        parts.append(f"output:\n{stdout}")
    if stderr:
        parts.append(f"stderr:\n{stderr}")
    parts.append(f"result: {output_repr}")
    return "\n".join(parts)


@workflow.defn(name="RunScriptWorkflow")
class RunScriptWorkflow:
    @workflow.run
    async def run(self, message: RunScript) -> str:
        return await self._run_script(message.script, message.session_id)

    async def _run_script(self, script: str, session_id: str) -> str:
        """Drive a script to completion via the suspend-at-host-call loop, then return the reply.

        The Workflow never runs Monty itself. It calls ``monty_start`` once to get the
        script running, then repeatedly: when a step comes back awaiting a batch of tool
        calls, it runs them as concurrent Activities (``_dispatch_one`` via asyncio.gather)
        and feeds the results into ``monty_resume`` — until a step comes back ``done``. The
        printed output of every step is accumulated and returned alongside the script's final
        value. A Monty syntax/runtime error comes back as ``step.error`` (a bad script is normal
        input, not a Workflow failure) and becomes a plain reply.
        """
        log = workflow.logger
        log.info(
            "monty: starting stepwise run (script_len=%d)\n--- script ---\n%s\n--- end ---",
            len(script),
            script,
        )

        stdout_parts: list[str] = []
        stderr_parts: list[str] = []
        stubs: str = await workflow.execute_activity(
            activities.get_catalog_stub,
            start_to_close_timeout=_ACTIVITY_TIMEOUT,
            summary="load tool stubs",
        )
        step: MontyStep = await workflow.execute_activity(
            monty_start,
            MontyStartInput(script=script, stubs=stubs),
            start_to_close_timeout=_MONTY_STEP_TIMEOUT,
            summary="start script",
        )
        stdout_parts.append(step.stdout)
        stderr_parts.append(step.stderr)

        # Accumulate call metadata across steps so a pending_call_id created in an earlier
        # step (awaited out of creation order) is still resolvable.
        call_meta: dict[int, PendingCall] = {}
        step_no = 0
        while not step.done:
            step_no += 1
            for c in step.calls:
                call_meta[c.call_id] = c
            pending = step.pending_call_ids
            log.info(
                "monty: step %d dispatching %d tool call(s) concurrently: %s",
                step_no,
                len(pending),
                [call_meta[cid].function_name for cid in pending],
            )
            # Run the whole awaited batch as concurrent Activities — this is the parallelism.
            results = await asyncio.gather(
                *[self._dispatch_one(call_meta[cid], session_id) for cid in pending]
            )
            log.info("monty: step %d batch complete, resuming sandbox", step_no)
            step = await workflow.execute_activity(
                monty_resume,
                MontyResumeInput(snapshot=step.snapshot, results=list(results)),
                start_to_close_timeout=_MONTY_STEP_TIMEOUT,
                summary=f"resume script (step {step_no})",
            )
            stdout_parts.append(step.stdout)
            stderr_parts.append(step.stderr)

        if step.error:
            log.warning("monty: script error: %s", step.error)
            return f"Script error ({step.error})"

        # output_json is the script's final expression serialized by Monty; decode it so
        # the reply shows a native value rather than a JSON blob.
        output = json.loads(step.output_json) if step.output_json else None
        stdout = "".join(stdout_parts).strip()
        stderr = "".join(stderr_parts).strip()
        log.info("monty: run complete after %d host call(s); returning reply", step_no)
        return _format_reply(stdout, stderr, repr(output))

    async def _dispatch_one(self, call: PendingCall, session_id: str) -> CallResult:
        """Run one awaited upstream tool call as an Activity, mapping it to a CallResult
        (success → return value; failure → a catchable exception for that call_id).

        Called via ``asyncio.gather`` for a whole awaited batch, so the batch runs as
        concurrent Activities.
        """
        request = CallToolRequest(
            name=call.function_name, arguments=call.kwargs, session_id=session_id
        )
        try:
            result = await workflow.execute_activity(
                activities.call_tool_activity,
                request,
                start_to_close_timeout=_ACTIVITY_TIMEOUT,
                retry_policy=_TOOL_RETRY,
                summary=_call_summary(call),
            )
        except ActivityError as e:
            # Retries for a transient upstream failure (rate limit / 5xx) were exhausted.
            # Surface it to the script as a catchable RuntimeError rather than failing the
            # whole workflow, keeping the "a tool failure is data" contract.
            cause = e.cause
            message = str(cause) if cause else str(e)
            return CallResult(
                call_id=call.call_id,
                exc_type="RuntimeError",
                message=f"tool call failed after retries: {message}",
            )
        if result.ok:
            return CallResult(call_id=call.call_id, return_value=result.result)
        return CallResult(
            call_id=call.call_id,
            exc_type="RuntimeError",
            message=result.error or "tool failed",
        )


@workflow.defn(name="GetCatalogWorkflow")
class GetCatalogWorkflow:
    """Serve the live tool catalog from the backend's registry to the stdio server over Temporal."""

    @workflow.run
    async def run(self) -> Catalog:
        return await workflow.execute_activity(
            activities.get_catalog,
            start_to_close_timeout=_ACTIVITY_TIMEOUT,
            summary="get catalog",
        )
