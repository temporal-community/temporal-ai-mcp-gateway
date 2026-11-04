"""Worker wiring for the durable MCP gateway: the task queue and a Worker factory.

The single source of truth for how a Worker is registered. Both the stdio server
(``stdio/run.py``) and the workflow debug harness (``scripts/run_workflow.py``) build
their Worker via :func:`new_worker`, so the workflow/activity registration lives in one
place instead of being duplicated per entry point.
"""

from __future__ import annotations

from temporalio.client import Client
from temporalio.worker import Worker

from . import activities, config
from .monty_activities import monty_resume, monty_start
from .workflow import GetCatalogWorkflow, RunScriptWorkflow

TASK_QUEUE = "durable-mcp-gateway"


def new_worker(client: Client) -> Worker:
    """Build a Worker that polls :data:`TASK_QUEUE` for the durable script-runner.

    ``max_concurrent_activities`` bounds how many tool calls run in parallel: a script may
    ``asyncio.gather`` any number, but only this many execute at once (see config).
    """
    return Worker(
        client,
        task_queue=TASK_QUEUE,
        workflows=[RunScriptWorkflow, GetCatalogWorkflow],
        activities=[*activities.ALL_ACTIVITIES, monty_start, monty_resume],
        max_concurrent_activities=config.MAX_CONCURRENT_ACTIVITIES,
    )
