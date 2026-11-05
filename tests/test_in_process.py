"""Tests for --no-temporal mode: scripts run in this process against the stdio fixture upstream,
through the same Monty and tool-call functions the durable Workflow uses, with no Temporal."""

import asyncio
import os
import signal
import socket
import sys

import mcp.types as types
import pytest
from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client
from temporalio.client import Client

from durable_mcp_gateway import activities, config, upstreams
from durable_mcp_gateway.in_process import InProcessRunner
from stdio.server import build_no_temporal_server
from tests.test_oauth import _use_file_vault
from tests.test_workflow import fixture_upstreams  # noqa: F401 - pytest fixture

_ADD = (
    "import asyncio\n"
    "async def main():\n"
    "    r = await fixture_add(a=2, b=3)\n"
    '    print("called add")\n'
    "    return r\n"
    "asyncio.run(main())\n"
)


async def test_script_calls_real_upstream_tool(fixture_upstreams):
    await upstreams.setup_worker()
    lines: list[str] = []
    reply = await InProcessRunner(lines.append).run_script(_ADD, "")
    assert reply == "output:\ncalled add\nresult: {'sum': 5}"
    assert len(lines) == 1
    assert "fixture_add" in lines[0] and lines[0].endswith("ok")


async def test_upstream_tool_failure_raises_catchable_exception(fixture_upstreams):
    await upstreams.setup_worker()
    script = (
        "import asyncio\n"
        "async def main():\n"
        "    try:\n"
        "        await fixture_boom()\n"
        "        return 'no error'\n"
        "    except RuntimeError as e:\n"
        "        return 'caught: ' + str(e)\n"
        "asyncio.run(main())\n"
    )
    reply = await InProcessRunner().run_script(script, "")
    assert "caught:" in reply
    assert "intentional failure" in reply


async def test_raised_tool_call_failure_is_caught_without_retry(fixture_upstreams):
    # Unreachable, call_tool_activity raises for the Workflow to retry; here the script gets it.
    await upstreams.setup_worker()
    upstreams.get_tool("fixture_add").server_cfg = {
        "name": "fixture",
        "transport": "streamable-http",
        "url": "http://127.0.0.1:1/mcp",
    }
    script = (
        "import asyncio\n"
        "async def main():\n"
        "    try:\n"
        "        return await fixture_add(a=2, b=3)\n"
        "    except RuntimeError as e:\n"
        "        return 'caught: ' + str(e)\n"
        "asyncio.run(main())\n"
    )
    reply = await InProcessRunner().run_script(script, "")
    assert "caught: tool call failed:" in reply
    assert "ConnectError" in reply


async def test_uncaught_tool_failure_becomes_script_error(fixture_upstreams):
    await upstreams.setup_worker()
    script = (
        "import asyncio\n"
        "async def main():\n"
        "    return await fixture_boom()\n"
        "asyncio.run(main())\n"
    )
    reply = await InProcessRunner().run_script(script, "")
    assert reply.startswith("Script error")
    assert "intentional failure" in reply


async def test_syntax_error_script_is_data(fixture_upstreams):
    reply = await InProcessRunner().run_script("def (", "")
    assert reply.startswith("Script error")


async def test_tool_calls_capped_at_worker_activity_limit(fixture_upstreams, monkeypatch):
    await upstreams.setup_worker()
    monkeypatch.setattr(config, "MAX_CONCURRENT_ACTIVITIES", 2)
    in_flight = peak = 0
    call_tool = activities.call_tool_activity

    async def counting(request):
        nonlocal in_flight, peak
        in_flight += 1
        peak = max(peak, in_flight)
        try:
            return await call_tool(request)
        finally:
            in_flight -= 1

    monkeypatch.setattr(activities, "call_tool_activity", counting)
    script = (
        "import asyncio\n"
        "async def main():\n"
        "    return len(await asyncio.gather(*[fixture_add(a=i, b=1) for i in range(5)]))\n"
        "asyncio.run(main())\n"
    )
    reply = await InProcessRunner().run_script(script, "")
    assert reply == "result: 5"
    assert peak == 2


async def _call(server, name, arguments):
    handler = server.request_handlers[types.CallToolRequest]
    request = types.CallToolRequest(
        method="tools/call",
        params=types.CallToolRequestParams(name=name, arguments=arguments),
    )
    return (await handler(request)).root.content[0].text


async def test_no_temporal_server_needs_no_temporal_client(
    fixture_upstreams, tmp_path, monkeypatch
):
    async def no_connect(*args, **kwargs):
        raise AssertionError("no-temporal mode connected to Temporal")

    monkeypatch.setattr(Client, "connect", no_connect)
    _use_file_vault(tmp_path, monkeypatch)
    await upstreams.setup_worker()
    server = build_no_temporal_server()

    listing = await server.request_handlers[types.ListToolsRequest](
        types.ListToolsRequest(method="tools/list")
    )
    tools = {t.name: t.description for t in listing.root.tools}
    assert set(tools) == {"run_script", "list_upstream_tools", "list_upstream_tools_as_json"}
    for description in tools.values():
        assert "Temporal" not in description
        assert "backend" not in description
        assert "durabl" not in description.lower()

    assert "async def fixture_add(" in await _call(server, "list_upstream_tools", {})
    assert "fixture.add" in await _call(server, "list_upstream_tools_as_json", {})
    reply = await _call(server, "run_script", {"script": _ADD})
    assert reply == "output:\ncalled add\nresult: {'sum': 5}"


def _free_port() -> int:
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


@pytest.mark.parametrize("no_temporal", [False, True])
async def test_http_transport_serves_tool_list(fixture_upstreams, tmp_path, no_temporal):
    port = _free_port()
    env = {
        **os.environ,
        "DURABLE_MCP_GATEWAY_HOME": str(fixture_upstreams),
        "DURABLE_MCP_GATEWAY_CRED_BACKEND": "file",
        "DURABLE_MCP_GATEWAY_CREDENTIALS_PATH": str(tmp_path / "creds.json"),
    }
    args = ["-m", "durable_mcp_gateway.cli", "http", "--port", str(port)]
    proc = await asyncio.create_subprocess_exec(
        sys.executable, *args, *(["--no-temporal"] if no_temporal else []),
        env=env, stderr=asyncio.subprocess.PIPE,
    )
    try:
        for _ in range(100):
            try:
                _, writer = await asyncio.open_connection("127.0.0.1", port)
            except OSError:
                await asyncio.sleep(0.1)
                continue
            writer.close()
            break
        async with streamable_http_client(f"http://127.0.0.1:{port}/mcp") as (read, write, _):
            async with ClientSession(read, write) as session:
                await session.initialize()
                names = {t.name for t in (await session.list_tools()).tools}
    finally:
        proc.send_signal(signal.SIGINT)
        _, stderr = await asyncio.wait_for(proc.communicate(), timeout=10)

    assert {"run_script", "list_upstream_tools", "list_upstream_tools_as_json"} <= names
    assert ("wait_script_result" in names) is not no_temporal
    assert ("in-flight work is lost" in stderr.decode()) is no_temporal
