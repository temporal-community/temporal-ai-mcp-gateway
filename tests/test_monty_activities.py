"""Unit tests for the Monty stepping + reply-formatting helpers."""

import pydantic_monty as monty
from temporalio.testing import ActivityEnvironment

from durable_mcp_gateway import monty_activities
from durable_mcp_gateway.monty_activities import MontyStartInput, monty_start
from durable_mcp_gateway.workflow import _format_reply

_STUB = '''from typing import Any, TypedDict


class FixtureAddResult(TypedDict):
    sum: int


async def fixture_add(*, a: int, b: int) -> FixtureAddResult:
    """Add two numbers."""
    ...


async def fixture_noout_a() -> Any:
    """Return a thing.

    Result fields seen in past calls: id: str, count: int. Merged across those calls,
    so it is neither complete nor guaranteed for any one call — check that a field is
    present before using it.
    """
    ...
'''


async def _start(script: str):
    return await ActivityEnvironment().run(
        monty_start, MontyStartInput(script=script, stubs=_STUB)
    )


class _FakeStreams:
    def __init__(self, entries):
        self._entries = entries

    @property
    def output(self):
        return self._entries


def test_split_streams_separates_stdout_and_stderr():
    # The pydantic-monty sandbox gives script code no way to emit to stderr, so a real run
    # can't produce interleaved streams; a hand-rolled log exercises the interleaving logic.
    streams = _FakeStreams(
        [("stdout", "a"), ("stderr", "x"), ("stdout", "b"), ("stderr", "y")]
    )
    stdout, stderr = monty_activities._split_streams(streams)
    assert stdout == "ab"
    assert stderr == "xy"


def test_split_streams_on_real_collectstreams_stdout():
    streams = monty.CollectStreams()
    monty.Monty('print("hi")\nprint("there")').start(print_callback=streams)
    stdout, stderr = monty_activities._split_streams(streams)
    assert stdout == "hi\nthere\n"
    assert stderr == ""


def test_monty_start_captures_stdout():
    streams = monty.CollectStreams()
    snap = monty.Monty('print("hello")\n1 + 1').start(print_callback=streams)
    stdout, stderr = monty_activities._split_streams(streams)
    assert stdout == "hello\n"
    assert stderr == ""
    assert isinstance(snap, monty.MontyComplete)


def test_format_reply_stdout_only():
    assert _format_reply("hi", "", "42") == "output:\nhi\nresult: 42"


def test_format_reply_stderr_only():
    assert _format_reply("", "oops", "42") == "stderr:\noops\nresult: 42"


def test_format_reply_both_streams():
    assert _format_reply("hi", "oops", "42") == "output:\nhi\nstderr:\noops\nresult: 42"


def test_format_reply_neither_stream():
    assert _format_reply("", "", "42") == "result: 42"


def _async(body: str) -> str:
    return "import asyncio\nasync def main():\n" + body + "\nasyncio.run(main())\n"


async def test_monty_start_awaits_tool_call_batch():
    step = await _start(_async('    r = await fixture_add(a=1, b=2)\n    return r["sum"]'))
    assert step.done is False
    assert step.error is None
    # The awaited call is reported as a batch: its metadata in `calls`, its id in pending.
    assert len(step.calls) == 1
    call = step.calls[0]
    assert call.function_name == "fixture_add"
    assert call.kwargs == {"a": 1, "b": 2}
    assert step.pending_call_ids == [call.call_id]


async def test_monty_start_unknown_return_accepts_any_field():
    # The field read here is deliberately absent from the docstring's shape.
    step = await _start(_async('    r = await fixture_noout_a()\n    return r["anything"]'))
    assert step.done is False
    assert step.error is None
    assert [c.function_name for c in step.calls] == ["fixture_noout_a"]


async def test_monty_start_unknown_tool_is_type_error():
    step = await _start(_async("    return await nope(a=1)"))
    assert step.done is True
    assert "MontyTypingError" in step.error


async def test_monty_start_missing_arg_is_type_error():
    step = await _start(_async("    return await fixture_add(a=1)"))
    assert step.done is True
    assert "MontyTypingError" in step.error


async def test_monty_start_wrong_type_is_type_error():
    step = await _start(_async('    return await fixture_add(a="x", b=2)'))
    assert step.done is True
    assert "MontyTypingError" in step.error
