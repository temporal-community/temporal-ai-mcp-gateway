"""Debug harness: run one script through RunScriptWorkflow, end to end.

Exercises just the durable workflow — no MCP / stdio layer — so you can iterate on the
suspend/resume loop directly. One-click: if the durable backend isn't already running at
the configured address it starts one automatically (using the same persistent-DB config as
``durable_mcp_gateway.serve``), runs the workflow, then shuts it down. If the backend IS
already running it connects to it and leaves it alone.

    uv run python scripts/run_workflow.py '<script>'

With no argument it runs a built-in example; pass a script that awaits a tool function (e.g. ``import asyncio; asyncio.run(fixture_add(a=1, b=2))``).
"""

from __future__ import annotations

import argparse
import asyncio
import os
from uuid import uuid4

from temporalio.client import Client
from temporalio.contrib.pydantic import pydantic_data_converter
from temporalio.testing import WorkflowEnvironment

from durable_mcp_gateway import config, upstreams
from durable_mcp_gateway.models import RunScript
from durable_mcp_gateway.worker import TASK_QUEUE, new_worker
from durable_mcp_gateway.workflow import RunScriptWorkflow

# Self-contained so the harness runs regardless of configured upstreams.
_EXAMPLE_SCRIPT = """\
xs = [i * i for i in range(5)]
print(f"squares: {xs}")
sum(xs)
"""


async def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "script",
        nargs="?",
        default=_EXAMPLE_SCRIPT,
        help="Python script to run in the sandbox (defaults to a built-in example).",
    )
    args = parser.parse_args()

    # Populate the upstream registry before the Worker
    # hosts the tool-call Activity — same discovery path the backend uses.
    await upstreams.setup_worker()

    # Try the already-running backend first; start one if it isn't up.
    env: WorkflowEnvironment | None = None
    try:
        client = await Client.connect(
            config.TEMPORAL_ADDRESS, data_converter=pydantic_data_converter
        )
        await client.service_client.check_health()
        print(f"[run_workflow] using existing backend at {config.TEMPORAL_ADDRESS}")
    except Exception:
        print(
            f"[run_workflow] no backend at {config.TEMPORAL_ADDRESS}; "
            f"starting one (downloads binary on first run)..."
        )
        os.makedirs(os.path.dirname(config.DB_PATH), exist_ok=True)
        env = await WorkflowEnvironment.start_local(
            namespace=config.TEMPORAL_NAMESPACE,
            data_converter=pydantic_data_converter,
            ip=config.TEMPORAL_HOST,
            port=config.TEMPORAL_PORT,
            ui=True,
            ui_port=config.TEMPORAL_UI_PORT,
            dev_server_database_filename=config.DB_PATH,
        )
        client = env.client
        print(f"[run_workflow] backend ready at {config.TEMPORAL_ADDRESS}")

    try:
        async with new_worker(client):
            handle = await client.start_workflow(
                RunScriptWorkflow.run,
                RunScript(script=args.script),
                id=f"run-script-{uuid4()}",
                task_queue=TASK_QUEUE,
            )
            print(await handle.result())
    finally:
        if env is not None:
            print("[run_workflow] shutting down backend")
            await env.shutdown()


if __name__ == "__main__":
    asyncio.run(main())
