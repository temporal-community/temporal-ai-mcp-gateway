"""Tests for the downstream MCP server the gateway exposes."""

import json

import mcp.types as types
import pytest
from temporalio.client import WorkflowFailureError
from temporalio.exceptions import ApplicationError, TimeoutType
from temporalio.exceptions import TimeoutError as TemporalTimeoutError

from durable_mcp_gateway import config
from stdio.server import BackendUnavailable, build_server


async def _failing_client():
    raise BackendUnavailable("connection refused")


class _ExecuteFailsClient:
    """A connected client whose ``execute_workflow`` raises a chosen failure."""

    def __init__(self, error: BaseException):
        self._error = error

    async def execute_workflow(self, *args, **kwargs):
        raise self._error


async def _call(server, name):
    result = await _call_result(server, name)
    return result.content[0].text


async def _call_result(server, name):
    handler = server.request_handlers[types.CallToolRequest]
    request = types.CallToolRequest(
        method="tools/call",
        params=types.CallToolRequestParams(name=name, arguments={}),
    )
    result = await handler(request)
    return result.root


@pytest.mark.asyncio
async def test_list_upstream_tools_backend_unavailable_returns_actionable_message():
    server = build_server(_failing_client, task_queue="q")
    text = await _call(server, "list_upstream_tools")
    assert config.TEMPORAL_ADDRESS in text
    assert config.BACKEND_DOWN_HINT in text


@pytest.mark.asyncio
async def test_list_upstream_tools_as_json_backend_unavailable_returns_actionable_note():
    server = build_server(_failing_client, task_queue="q")
    text = await _call(server, "list_upstream_tools_as_json")
    payload = json.loads(text)
    assert payload["tools"] == []
    assert config.TEMPORAL_ADDRESS in payload["note"]
    assert config.BACKEND_DOWN_HINT in payload["note"]


async def _connecting_client(error):
    client = _ExecuteFailsClient(error)

    async def _get_client():
        return client

    return _get_client


@pytest.mark.asyncio
async def test_catalog_execution_timeout_degrades_to_actionable_message():
    error = WorkflowFailureError(
        cause=TemporalTimeoutError(
            "timed out", type=TimeoutType.START_TO_CLOSE, last_heartbeat_details=[]
        )
    )
    server = build_server(await _connecting_client(error), task_queue="q")
    text = await _call(server, "list_upstream_tools")
    assert config.BACKEND_DOWN_HINT in text


@pytest.mark.asyncio
async def test_catalog_render_failure_propagates_not_masked():
    # A genuine catalog-render failure must surface as an error, not be masked as the
    # actionable "start the backend" message reserved for a timed-out/down backend.
    error = WorkflowFailureError(cause=ApplicationError("boom"))
    server = build_server(await _connecting_client(error), task_queue="q")

    result = await _call_result(server, "list_upstream_tools")
    assert result.isError
    assert config.BACKEND_DOWN_HINT not in result.content[0].text
