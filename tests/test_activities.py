"""Tests for call_tool_activity's error handling: the retryable-vs-terminal classification,
and a session dropped out from under a call by a Worker that is stopping."""

from contextlib import asynccontextmanager

import anyio
import pytest
from temporalio.activity import ActivityCancellationDetails
from temporalio.testing import ActivityEnvironment

from durable_mcp_gateway import upstreams
from durable_mcp_gateway.activities import (
    RetryableUpstreamError,
    _is_retryable_upstream_error,
    call_tool_activity,
)
from durable_mcp_gateway.models import CallToolRequest


# The real Notion 429 payload that motivated durable retries.
_NOTION_429 = (
    '{"name":"APIResponseError","code":"rate_limited","status":429,'
    '"body":"You have been rate limited","additional_data":'
    '{"rate_limit_reason":"collection_router_upstream_429","retry_after":"30"}}'
)


def test_retryable_rate_limit_and_5xx():
    assert _is_retryable_upstream_error(_NOTION_429)
    assert _is_retryable_upstream_error("Server returned status 503 Service Unavailable")
    assert _is_retryable_upstream_error("HTTP 502 Bad Gateway")
    assert _is_retryable_upstream_error("upstream code 500 internal error")
    assert _is_retryable_upstream_error("connection reset by peer")
    assert _is_retryable_upstream_error("Too Many Requests")


def test_retryable_connection_never_established():
    # A connection that never came up is as transient as one that broke mid-flight. These are
    # the reprs _exc_text flattens, as httpx and socket actually render them.
    assert _is_retryable_upstream_error(
        "ConnectError('[Errno 8] nodename nor servname provided, or not known')"
    )
    assert _is_retryable_upstream_error("ConnectError('[Errno 61] Connection refused')")
    assert _is_retryable_upstream_error("ConnectError('[Errno 51] Network is unreachable')")
    assert _is_retryable_upstream_error("ConnectError('[Errno 65] No route to host')")
    assert _is_retryable_upstream_error(
        "ConnectError('[SSL: SSLV3_ALERT_HANDSHAKE_FAILURE] handshake failure')"
    )
    assert _is_retryable_upstream_error("ConnectTimeout('timed out')")
    assert _is_retryable_upstream_error("PoolTimeout('')")
    assert _is_retryable_upstream_error("gaierror(-3, 'Temporary failure in name resolution')")
    assert _is_retryable_upstream_error("OSError(-2, 'Name or service not known')")


def test_not_retryable_terminal_errors():
    # Genuine tool errors must stay ok=False (no retry).
    assert not _is_retryable_upstream_error('{"status":400,"message":"bad arguments"}')
    assert not _is_retryable_upstream_error("status 404 not found")
    assert not _is_retryable_upstream_error("page does not exist")
    assert not _is_retryable_upstream_error("")


def test_bare_number_without_http_context_is_not_retryable():
    # A plain "500" in a tool's data/message must not trigger retries.
    assert not _is_retryable_upstream_error("processed 500 records successfully")


_TOOL = upstreams.UpstreamTool(
    namespaced_name="fixture.add",
    server_name="fixture",
    tool_name="add",
    description="",
    input_schema={"type": "object"},
    output_schema=None,
    server_cfg={"transport": "stdio", "command": "never-run"},
    py_name="fixture_add",
    py_arg_map={},
)
_REQUEST = CallToolRequest(name="fixture_add", arguments={}, session_id="s")


def _register_dropping_session(monkeypatch, before_drop=lambda: None, exc=None):
    """Register one tool whose upstream session dies the moment a call opens it."""

    @asynccontextmanager
    async def drop(*args, **kwargs):
        before_drop()
        raise exc if exc is not None else anyio.BrokenResourceError()
        yield  # unreachable; makes this an async generator

    monkeypatch.setattr(upstreams, "get_tool", lambda name: _TOOL)
    monkeypatch.setattr(upstreams, "upstream_session", drop)


async def test_dropped_session_is_a_tool_error(monkeypatch):
    _register_dropping_session(monkeypatch)
    result = await ActivityEnvironment().run(call_tool_activity, _REQUEST)
    assert not result.ok


async def test_dropped_session_outside_an_activity_is_a_tool_error(monkeypatch):
    # The --no-temporal runner calls the Activity function directly, with no Activity context.
    _register_dropping_session(monkeypatch)
    result = await call_tool_activity(_REQUEST)
    assert not result.ok
    assert "BrokenResourceError" in result.error


async def test_dropped_session_while_worker_stops_fails_the_activity(monkeypatch):
    # A stopping Worker tears the session down mid-call, so this drop has to be retried on
    # the next Worker rather than handed to the script as a tool error — otherwise a script
    # can't survive the Worker restart the durable loop exists to survive.
    env = ActivityEnvironment()
    _register_dropping_session(
        monkeypatch,
        lambda: env.cancel(ActivityCancellationDetails(worker_shutdown=True)),
    )
    with pytest.raises(anyio.BrokenResourceError):
        await env.run(call_tool_activity, _REQUEST)


async def test_connect_failure_fails_the_activity(monkeypatch):
    # The MCP client's task group wraps a transport failure, so a connect error reaches the
    # classifier only through _exc_text's flattening. It has to fail the Activity: handed to
    # the script as a tool error, a momentary DNS blip becomes a permanently failed tool.
    _register_dropping_session(
        monkeypatch,
        exc=ExceptionGroup(
            "unhandled errors in a TaskGroup",
            [OSError(8, "nodename nor servname provided, or not known")],
        ),
    )
    with pytest.raises(RetryableUpstreamError):
        await ActivityEnvironment().run(call_tool_activity, _REQUEST)
