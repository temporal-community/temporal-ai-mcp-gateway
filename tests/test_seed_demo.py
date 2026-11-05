"""Tests for the ``seed-demo`` command against a fake Notion MCP session."""

import json
import sys
from contextlib import asynccontextmanager

import mcp.types as types
import pytest

from durable_mcp_gateway import cli, config, seed_demo, upstreams

DATA_SOURCE_ID = "11111111-2222-3333-4444-555555555555"
NOTION_CFG = {
    "name": "notion",
    "transport": "streamable-http",
    "url": "https://mcp.notion.com/mcp",
    "auth": {"type": "oauth"},
}


def _result(text: str, is_error: bool = False) -> types.CallToolResult:
    return types.CallToolResult(
        content=[types.TextContent(type="text", text=text)], isError=is_error
    )


class _FakeNotion:
    def __init__(self) -> None:
        self.calls: list[tuple[str, dict]] = []
        self.fail_tool: str | None = None

    async def call_tool(self, name: str, arguments: dict) -> types.CallToolResult:
        self.calls.append((name, arguments))
        if name == self.fail_tool:
            return _result('{"status":400,"message":"bad page"}', is_error=True)
        if name == "notion-create-database":
            return _result(f'<data-source url="{{{{collection://{DATA_SOURCE_ID}}}}}">')
        return _result('{"pages": []}')

    def pages_created(self) -> list[dict]:
        return [p for name, args in self.calls if name == "notion-create-pages" for p in args["pages"]]


@pytest.fixture
def notion(tmp_path, monkeypatch):
    monkeypatch.setattr(config, "CRED_BACKEND", "file")
    monkeypatch.setattr(config, "CREDENTIALS_PATH", str(tmp_path / "creds.json"))
    monkeypatch.setattr(upstreams, "UPSTREAMS_PATH", str(tmp_path / "upstreams.json"))
    (tmp_path / "upstreams.json").write_text(json.dumps({"servers": [NOTION_CFG]}))
    fake = _FakeNotion()

    @asynccontextmanager
    async def session(server_cfg, token_storage=None):
        assert server_cfg["name"] == "notion" and token_storage is not None
        yield fake

    monkeypatch.setattr(upstreams, "upstream_session", session)
    return fake


def _write_dump(directory, files: dict[str, str]) -> None:
    directory.mkdir()
    for name, text in files.items():
        (directory / name).write_text(text)


def test_seed_demo_creates_database_and_every_page(notion, tmp_path, monkeypatch, capsys):
    dump = tmp_path / "demo-db"
    _write_dump(
        dump,
        {
            "2-second.md": (
                "---\nName: Second: Part Two\nOwner: B\nStatus: Shipped\n"
                "Last Updated: 2026-02-02\n---\n\n## Body\n\n---\n\n- two\n"
            ),
            "1-first.md": (
                "---\nName: First\nOwner: A\nStatus: Draft\nLast Updated: 2026-01-01\n---\n\n"
                "## Body\n\n- one\n"
            ),
            "3-third.md": (
                "---\nName: Third\nOwner: C\nStatus: Parked\nLast Updated: 2026-03-03\n---\n\n"
                "Three.\n"
            ),
        },
    )
    monkeypatch.setattr(seed_demo, "DEMO_DB_DIR", dump)
    monkeypatch.setattr(seed_demo, "BATCH_SIZE", 2)

    seed_demo.seed_demo("https://www.notion.so/team/Demo-4058fc56773881868935da8b4bf9f765?pvs=4")

    name, args = notion.calls[0]
    assert name == "notion-create-database"
    assert args["parent"] == {"page_id": "4058fc56773881868935da8b4bf9f765"}
    assert args["title"] == "Product One-Pagers (Demo)"
    for column in (
        '"Name" TITLE',
        '"Owner" RICH_TEXT',
        "\"Status\" SELECT('Draft':gray, 'In Review':yellow, 'Approved':green, "
        "'Shipped':blue, 'Parked':red)",
        '"Last Updated" DATE',
    ):
        assert column in args["schema"]

    batches = [args for name, args in notion.calls[1:]]
    assert [name for name, _ in notion.calls[1:]] == ["notion-create-pages"] * 2
    assert [len(b["pages"]) for b in batches] == [2, 1]
    assert all(b["parent"] == {"data_source_id": DATA_SOURCE_ID} for b in batches)

    def page(name, owner, status, date, content):
        return {
            "properties": {
                "Name": name,
                "Owner": owner,
                "Status": status,
                "date:Last Updated:start": date,
                "date:Last Updated:is_datetime": 0,
            },
            "content": content,
        }

    assert notion.pages_created() == [
        page("First", "A", "Draft", "2026-01-01", "## Body\n\n- one"),
        page("Second: Part Two", "B", "Shipped", "2026-02-02", "## Body\n\n---\n\n- two"),
        page("Third", "C", "Parked", "2026-03-03", "Three."),
    ]
    assert capsys.readouterr().out.splitlines()[-1] == f"collection://{DATA_SOURCE_ID}"


def test_shipped_dump_seeds_every_page(notion):
    seed_demo.seed_demo("https://app.notion.com/p/4058fc56773881868935da8b4bf9f765")

    pages = notion.pages_created()
    assert len(pages) == len(list(seed_demo.DEMO_DB_DIR.glob("*.md"))) == 300
    for p in pages:
        props = p["properties"]
        assert props["Name"] and props["Owner"] and props["date:Last Updated:start"]
        assert props["Status"] in {"Draft", "In Review", "Approved", "Shipped", "Parked"}
        assert p["content"].startswith("## ")


def test_seed_demo_not_connected_names_connect_command(notion, monkeypatch):
    @asynccontextmanager
    async def unauthorized(server_cfg, token_storage=None):
        raise ExceptionGroup(
            "unhandled errors in a TaskGroup",
            [upstreams.ReconnectRequired("needs authorization")],
        )
        yield

    monkeypatch.setattr(upstreams, "upstream_session", unauthorized)

    with pytest.raises(SystemExit, match="run: uv run durable-mcp-gateway connect notion"):
        seed_demo.seed_demo("https://app.notion.com/p/4058fc56773881868935da8b4bf9f765")


def test_seed_demo_stops_on_tool_error(notion, capsys):
    notion.fail_tool = "notion-create-pages"

    with pytest.raises(SystemExit, match="notion-create-pages failed: .*bad page"):
        seed_demo.seed_demo("https://app.notion.com/p/4058fc56773881868935da8b4bf9f765")
    assert [name for name, _ in notion.calls] == ["notion-create-database", "notion-create-pages"]
    assert f"collection://{DATA_SOURCE_ID}" in capsys.readouterr().err


@pytest.mark.parametrize(
    "parent",
    [
        "https://app.notion.com/p/4058fc56773881868935da8b4bf9f765",
        "https://www.notion.so/team/Demo-4058fc56773881868935da8b4bf9f765?pvs=4",
        "4058fc56-7738-8186-8935-da8b4bf9f765",
    ],
)
def test_page_id_from_parent(parent):
    assert seed_demo._page_id(parent) == "4058fc56773881868935da8b4bf9f765"


def test_page_id_rejects_url_without_one():
    with pytest.raises(SystemExit, match="no Notion page ID"):
        seed_demo._page_id("https://www.notion.so/team/Demo")


def test_cli_dispatches_seed_demo(monkeypatch):
    seen = []
    monkeypatch.setattr(seed_demo, "seed_demo", seen.append)
    monkeypatch.setattr(config, "configure_logging", lambda verbose: None)
    monkeypatch.setattr(sys, "argv", ["durable-mcp-gateway", "seed-demo", "--parent", "P"])

    cli.main()

    assert seen == ["P"]
