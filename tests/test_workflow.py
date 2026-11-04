"""End-to-end tests for the durable suspend/resume loop.

Each test runs RunScriptWorkflow against a real WorkflowEnvironment + Worker (plain
pydantic converter) and drives it like a client would: start the Workflow, await the
result. The tool tests point an ``upstreams.json`` (under a tmp home) at the local stdio
:mod:`tests.fixture_server`, so a script that calls ``fixture_add(a=2, b=3)`` proves the
sandbox suspended, the Activity ran a REAL upstream tool, and the sandbox resumed with the
unwrapped result.
"""

import json
import os
import sys
from uuid import uuid4

import pytest
import pytest_asyncio
from temporalio.contrib.pydantic import pydantic_data_converter
from temporalio.testing import WorkflowEnvironment
from temporalio.worker import Worker

from durable_mcp_gateway import activities, upstreams
from durable_mcp_gateway.models import RunScript
from durable_mcp_gateway.monty_activities import PendingCall, monty_resume, monty_start
from durable_mcp_gateway.workflow import GetCatalogWorkflow, RunScriptWorkflow, _call_summary


def test_call_summary_is_the_upstream_function_name():
    call = PendingCall(call_id=1, function_name="notion_fetch", args=[], kwargs={"id": "abc"})
    assert _call_summary(call) == "notion_fetch"

FIXTURE_SERVER = os.path.join(os.path.dirname(__file__), "fixture_server.py")


@pytest.fixture
def fixture_upstreams(tmp_path, monkeypatch):
    """Write an upstreams.json pointing at the fixture server and discover it."""
    d = tmp_path / "home"
    d.mkdir()
    monkeypatch.setattr(upstreams, "HOME_DIR", str(d))
    monkeypatch.setattr(upstreams, "UPSTREAMS_PATH", str(d / "upstreams.json"))
    monkeypatch.setattr(upstreams, "SHAPES_PATH", str(d / "upstreams-shapes.json"))
    monkeypatch.setattr(upstreams, "_shapes_cache", None)
    (d / "upstreams.json").write_text(
        json.dumps(
            {
                "servers": [
                    {
                        "name": "fixture",
                        "transport": "stdio",
                        "command": sys.executable,
                        "args": [FIXTURE_SERVER],
                    }
                ]
            }
        )
    )
    upstreams._REGISTRY.clear()
    yield d
    upstreams._REGISTRY.clear()


@pytest_asyncio.fixture
async def client_and_queue():
    env = await WorkflowEnvironment.start_time_skipping(
        data_converter=pydantic_data_converter
    )
    try:
        task_queue = f"durable-mcp-gateway-test-{uuid4()}"
        async with Worker(
            env.client,
            task_queue=task_queue,
            workflows=[RunScriptWorkflow, GetCatalogWorkflow],
            activities=[*activities.ALL_ACTIVITIES, monty_start, monty_resume],
        ):
            yield env.client, task_queue
    finally:
        await env.shutdown()


async def _run(client, task_queue, script: str) -> str:
    handle = await client.start_workflow(
        RunScriptWorkflow.run,
        RunScript(script=script),
        id=f"test-{uuid4()}",
        task_queue=task_queue,
    )
    return await handle.result()


async def test_script_calls_real_upstream_tool(client_and_queue, fixture_upstreams):
    await upstreams.discover_upstreams()
    client, task_queue = client_and_queue
    # Result is the raw upstream value, no {ok,result,error} envelope.
    script = (
        "import asyncio\n"
        "async def main():\n"
        "    r = await fixture_add(a=2, b=3)\n"
        '    print("called add")\n'
        "    return r\n"
        "asyncio.run(main())\n"
    )
    reply = await _run(client, task_queue, script)
    assert "called add" in reply
    assert "{'sum': 5}" in reply
    assert "ok" not in reply


async def test_upstream_tool_failure_raises_catchable_exception(
    client_and_queue, fixture_upstreams
):
    await upstreams.discover_upstreams()
    client, task_queue = client_and_queue
    script = (
        "import asyncio\n"
        "async def main():\n"
        "    try:\n"
        "        await fixture_boom()\n"
        "        return 'no error'\n"
        "    except Exception as e:\n"
        "        return 'caught: ' + str(e)\n"
        "asyncio.run(main())\n"
    )
    reply = await _run(client, task_queue, script)
    assert "caught:" in reply
    assert "intentional failure" in reply


async def test_uncaught_tool_failure_becomes_script_error(
    client_and_queue, fixture_upstreams
):
    await upstreams.discover_upstreams()
    client, task_queue = client_and_queue
    script = (
        "import asyncio\n"
        "async def main():\n"
        "    return await fixture_boom()\n"
        "asyncio.run(main())\n"
    )
    reply = await _run(client, task_queue, script)
    assert "Script error" in reply
    assert "intentional failure" in reply


async def test_unusable_input_schema_skips_validation(client_and_queue, fixture_upstreams):
    await upstreams.discover_upstreams()
    # Unusable input schema → Activity warns and skips validation; the call still runs.
    upstreams.get_tool("fixture_add").input_schema = {
        "type": "not-a-real-json-schema-type",
        "properties": {"a": {"type": "integer"}, "b": {"type": "integer"}},
        "required": ["a", "b"],
    }
    client, task_queue = client_and_queue
    script = (
        "import asyncio\n"
        "async def main():\n"
        "    return await fixture_add(a=2, b=3)\n"
        "asyncio.run(main())\n"
    )
    reply = await _run(client, task_queue, script)
    assert "{'sum': 5}" in reply
    assert "did not match schema" not in reply


async def test_unknown_tool_is_type_error(client_and_queue, fixture_upstreams):
    await upstreams.discover_upstreams()
    client, task_queue = client_and_queue
    script = "fixture_nope()"
    reply = await _run(client, task_queue, script)
    assert "Script error" in reply
    assert "MontyTypingError" in reply


async def test_wrong_argument_type_is_type_error(client_and_queue, fixture_upstreams):
    await upstreams.discover_upstreams()
    client, task_queue = client_and_queue
    script = 'fixture_add(a="x", b=1)'
    reply = await _run(client, task_queue, script)
    assert "Script error" in reply
    assert "MontyTypingError" in reply


async def test_stdout_in_reply(client_and_queue, fixture_upstreams):
    client, task_queue = client_and_queue
    reply = await _run(client, task_queue, 'print("hi there")\n42')
    assert "output:\nhi there" in reply
    assert "result: 42" in reply
    # No stderr was produced, so the stderr block is omitted.
    assert "stderr:" not in reply


async def test_syntax_error_script_is_data_not_failure(client_and_queue, fixture_upstreams):
    client, task_queue = client_and_queue
    reply = await _run(client, task_queue, "def (")
    assert "Script error" in reply


async def test_get_catalog_workflow_returns_stub_and_tools(client_and_queue, fixture_upstreams):
    await upstreams.discover_upstreams()
    client, task_queue = client_and_queue
    catalog = await client.execute_workflow(
        GetCatalogWorkflow.run,
        id=f"test-{uuid4()}",
        task_queue=task_queue,
    )
    assert "async def fixture_add(" in catalog.stub
    names = {t["name"] for t in catalog.tools}
    assert {"fixture.add", "fixture.boom"} <= names
