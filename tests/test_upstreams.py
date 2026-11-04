"""Tests for upstream config loading, discovery, and the registry.

The discovery tests point an ``upstreams.json`` (under a tmp home, via DURABLE_MCP_GATEWAY_HOME)
at the local stdio :mod:`tests.fixture_server`, so they exercise the real connect/list path
with no network.
"""

import ast
import json
import os
import re
import sys

import pytest
from mcp import ClientSession

from durable_mcp_gateway import upstreams
from durable_mcp_gateway.activities import call_tool_activity
from durable_mcp_gateway.models import CallToolRequest
from durable_mcp_gateway.monty_activities import MontyStartInput, monty_start

FIXTURE_SERVER = os.path.join(os.path.dirname(__file__), "fixture_server.py")


def _fixture_server_cfg(name: str = "fixture", skip: list[str] | None = None) -> dict:
    return {
        "name": name,
        "transport": "stdio",
        "command": sys.executable,
        "args": [FIXTURE_SERVER],
        "skip": skip or [],
    }


@pytest.fixture
def home(tmp_path, monkeypatch):
    """Redirect upstreams.py's path constants at a tmp home and reset module state."""
    d = tmp_path / "home"
    d.mkdir()
    monkeypatch.setattr(upstreams, "HOME_DIR", str(d))
    monkeypatch.setattr(upstreams, "UPSTREAMS_PATH", str(d / "upstreams.json"))
    monkeypatch.setattr(upstreams, "SHAPES_PATH", str(d / "upstreams-shapes.json"))
    monkeypatch.setattr(upstreams, "_shapes_cache", None)
    upstreams._REGISTRY.clear()
    yield d
    upstreams._REGISTRY.clear()


def _write_upstreams(home, servers: list[dict]) -> None:
    (home / "upstreams.json").write_text(json.dumps({"servers": servers}))


def test_expand_env_success(monkeypatch):
    monkeypatch.setenv("MY_TOKEN", "secret")
    assert upstreams.expand_env({"h": "${MY_TOKEN}", "xs": ["${MY_TOKEN}"]}) == {
        "h": "secret",
        "xs": ["secret"],
    }


def test_expand_env_unresolved_raises(monkeypatch):
    monkeypatch.delenv("DEFINITELY_UNSET_VAR", raising=False)
    with pytest.raises(RuntimeError, match="unresolved environment variable"):
        upstreams.expand_env("${DEFINITELY_UNSET_VAR}")


def test_expand_env_unresolved_bare_var_raises(monkeypatch):
    # os.path.expandvars leaves a brace-less ``$VAR`` literal; the check must still catch it.
    monkeypatch.delenv("DEFINITELY_UNSET_VAR", raising=False)
    with pytest.raises(RuntimeError, match="unresolved environment variable"):
        upstreams.expand_env("$DEFINITELY_UNSET_VAR")


def test_load_servers_expands_and_aborts_on_unresolved(home, monkeypatch):
    monkeypatch.delenv("DEFINITELY_UNSET_VAR", raising=False)
    _write_upstreams(
        home,
        [
            {
                "name": "x",
                "transport": "streamable-http",
                "url": "https://example/${DEFINITELY_UNSET_VAR}",
            }
        ],
    )
    with pytest.raises(RuntimeError, match="unresolved environment variable"):
        upstreams.load_servers()


def test_load_servers_expands_command_and_url(home, monkeypatch):
    monkeypatch.setenv("MY_HOST", "example.com")
    _write_upstreams(
        home,
        [{"name": "x", "transport": "streamable-http", "url": "https://${MY_HOST}/mcp"}],
    )
    [server] = upstreams.load_servers()
    assert server["url"] == "https://example.com/mcp"


def test_load_servers_absent_file_is_empty(home, caplog):
    with caplog.at_level("WARNING"):
        assert upstreams.load_servers() == []
    assert any("no upstreams config" in r.message for r in caplog.records)


def test_home_dir_override_resolves_paths(monkeypatch):
    # DURABLE_MCP_GATEWAY_HOME drives HOME_DIR and the path constants derived from it at import.
    # Reload in a fresh module namespace so the live ``upstreams`` module isn't mutated.
    import importlib.util

    monkeypatch.setenv("DURABLE_MCP_GATEWAY_HOME", "/tmp/custom-home")
    spec = importlib.util.spec_from_file_location("upstreams_override", upstreams.__file__)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    assert mod.HOME_DIR == "/tmp/custom-home"
    assert mod.UPSTREAMS_PATH == "/tmp/custom-home/upstreams.json"
    assert mod.SHAPES_PATH == "/tmp/custom-home/upstreams-shapes.json"


def test_warn_unsupported_auth_warns_on_unknown(caplog):
    cfg = {"name": "x", "auth": {"type": "saml"}}
    with caplog.at_level("WARNING"):
        upstreams._warn_unsupported_auth(cfg)
    assert any("not yet supported" in r.message for r in caplog.records)


def test_warn_unsupported_auth_silent_on_supported(caplog):
    # oauth is now handled by the vault-backed provider, so it must NOT warn.
    with caplog.at_level("WARNING"):
        upstreams._warn_unsupported_auth({"name": "x"})
        upstreams._warn_unsupported_auth({"name": "x", "auth": {"type": "bearer"}})
        upstreams._warn_unsupported_auth({"name": "x", "auth": {"type": "oauth"}})
    assert not any("not yet supported" in r.message for r in caplog.records)


def test_load_servers_validates_transport(home):
    _write_upstreams(home, [{"name": "x", "transport": "carrier-pigeon"}])
    with pytest.raises(upstreams.UpstreamConfigError, match="transport must be one of"):
        upstreams.load_servers()


async def test_discover_registers_fixture_tools(home):
    _write_upstreams(home, [_fixture_server_cfg()])
    await upstreams.discover_upstreams()
    add = upstreams.get_tool("fixture_add")
    assert add is not None
    assert add.namespaced_name == "fixture.add"
    assert add.tool_name == "add"
    assert add.output_schema is not None
    assert upstreams.get_tool("fixture_boom") is not None


async def test_tool_without_output_schema_registers_with_unknown_return(home):
    _write_upstreams(home, [_fixture_server_cfg()])
    await upstreams.discover_upstreams()
    noout = upstreams.get_tool("fixture_noout_a")
    assert noout is not None
    assert noout.output_schema is None
    assert "def fixture_noout_a() -> Any:" in upstreams.render_registry_stub()


async def test_discover_collision_warns_and_keeps_first(home, caplog):
    _write_upstreams(
        home,
        [
            _fixture_server_cfg(name="dup"),
            _fixture_server_cfg(name="dup"),
        ],
    )
    with caplog.at_level("WARNING"):
        await upstreams.discover_upstreams()
    assert any("duplicate tool" in r.message for r in caplog.records)
    # The first server registered every tool; the second server's all collided and were skipped.
    assert upstreams.get_tool("dup_add") is not None


async def test_unreachable_upstream_degrades(home, caplog):
    bad = {"name": "bad", "transport": "stdio", "command": sys.executable, "args": ["-c", "import sys; sys.exit(1)"]}
    _write_upstreams(home, [bad])
    with caplog.at_level("WARNING"):
        report = await upstreams.discover_upstreams()
    assert any("failed to connect upstream 'bad'" in r.message for r in caplog.records)
    # Discovery degrades (no raise) but must REPORT the failure so a strict caller (validate)
    # can fail on it rather than declaring success with zero tools.
    assert [name for name, _ in report.failed] == ["bad"]
    assert "bad" not in report.connected


async def test_discovery_report_lists_connected_counts(home):
    _write_upstreams(home, [_fixture_server_cfg()])
    report = await upstreams.discover_upstreams()
    assert report.failed == []
    assert report.connected == {"fixture": 4}  # add + boom + noout_a + noout_b


async def test_render_registry_catalog_from_registry(home):
    _write_upstreams(home, [_fixture_server_cfg()])
    await upstreams.discover_upstreams()
    catalog = upstreams.render_registry_catalog()
    by_name = {entry["name"]: entry for entry in catalog}
    assert {"fixture.add", "fixture.boom"} <= set(by_name)
    add = by_name["fixture.add"]
    assert add["py_name"] == "fixture_add"
    assert add["py_arg_map"] == {"a": "a", "b": "b"}


async def test_render_registry_stub_from_registry(home):
    _write_upstreams(home, [_fixture_server_cfg()])
    await upstreams.discover_upstreams()
    stub = upstreams.render_registry_stub()
    compile(stub, "catalog_stub.py", "exec")
    assert "def fixture_add(" in stub


def test_sanitize_identifier_dot_hyphen_and_leading_digit():
    assert upstreams.sanitize_identifier("notion.create_doc") == "notion_create_doc"
    assert upstreams.sanitize_identifier("github-mcp.create-issue") == "github_mcp_create_issue"
    assert upstreams.sanitize_identifier("3m.tool") == "_3m_tool"


def test_sanitize_identifier_keywords_get_suffixed():
    # A reserved keyword or soft keyword as a name would be a SyntaxError verbatim.
    assert upstreams.sanitize_identifier("return") == "return_"
    assert upstreams.sanitize_identifier("class") == "class_"
    assert upstreams.sanitize_identifier("import") == "import_"
    assert upstreams.sanitize_identifier("match") == "match_"
    assert upstreams.sanitize_identifier("") == "_"


def _tool(py_name, *, input_schema, output_schema, description="", py_arg_map=None):
    return upstreams.UpstreamTool(
        namespaced_name="s." + py_name,
        server_name="s",
        tool_name=py_name,
        description=description,
        input_schema=input_schema,
        output_schema=output_schema,
        server_cfg={},
        py_name=py_name,
        py_arg_map=py_arg_map or {},
    )


def _return_type(stub: str, py_name: str) -> str:
    return re.search(rf"def {py_name}\(.*?\) -> (\w+):", stub).group(1)


def _result_fields(stub: str, py_name: str) -> list[str]:
    """The ``key: type`` pairs of the TypedDict ``py_name`` returns, in declaration order."""
    cls = _return_type(stub, py_name)
    for node in ast.walk(ast.parse(stub)):
        if (
            isinstance(node, ast.Assign)
            and getattr(node.targets[0], "id", None) == cls
            and isinstance(node.value, ast.Call)
        ):
            fields = node.value.args[1]
            return [
                f"{k.value}: {ast.unparse(v)}"
                for k, v in zip(fields.keys, fields.values)
            ]
    raise AssertionError(f"no TypedDict {cls} in {stub}")


def test_render_catalog_stub_compiles_and_type_checks():
    import pydantic_monty as monty

    tool = _tool(
        "notion_create_doc",
        description="Create a doc.",
        input_schema={
            "type": "object",
            "properties": {"title": {"type": "string"}, "tags": {"type": "array", "items": {"type": "string"}}},
            "required": ["title"],
        },
        output_schema={"type": "object", "properties": {"url": {"type": "string"}}},
        py_arg_map={"title": "title", "tags": "tags"},
    )
    stub = upstreams.render_catalog_stub([tool])
    compile(stub, "catalog_stub.py", "exec")
    script = (
        "import asyncio\n"
        "async def main():\n"
        '    doc = await notion_create_doc(title="x")\n'
        '    return doc["url"]\n'
        "asyncio.run(main())\n"
    )
    snap = monty.Monty(script, type_check=True, type_check_stubs=stub).start(
        print_callback=monty.CollectStreams()
    )
    assert isinstance(snap, monty.FunctionSnapshot)
    assert snap.function_name == "notion_create_doc"
    with pytest.raises(monty.MontyTypingError):
        monty.Monty(
            "notion_create_doc(title=5)", type_check=True, type_check_stubs=stub
        ).start(print_callback=monty.CollectStreams())


def test_render_catalog_stub_keyword_names_compile_and_type_check():
    import pydantic_monty as monty

    # A property/field named like a keyword would be a verbatim SyntaxError poisoning the whole stub.
    tool = _tool(
        "kw_tool",
        input_schema={
            "type": "object",
            "properties": {"class": {"type": "string"}},
            "required": ["class"],
        },
        output_schema={"type": "object", "properties": {"import": {"type": "string"}}},
        py_arg_map={"class_": "class"},
    )
    stub = upstreams.render_catalog_stub([tool])
    compile(stub, "catalog_stub.py", "exec")
    script = (
        "import asyncio\n"
        "async def main():\n"
        '    r = await kw_tool(class_="x")\n'
        '    return r["import_"]\n'
        "asyncio.run(main())\n"
    )
    snap = monty.Monty(script, type_check=True, type_check_stubs=stub).start(
        print_callback=monty.CollectStreams()
    )
    assert isinstance(snap, monty.FunctionSnapshot)
    assert snap.function_name == "kw_tool"


def test_render_catalog_stub_colliding_arg_names_disambiguate():
    import pydantic_monty as monty

    # Colliding sanitized names must become distinct params, not a duplicate-param SyntaxError.
    tool = _tool(
        "collide",
        input_schema={
            "type": "object",
            "properties": {"first-arg": {"type": "string"}, "first_arg": {"type": "integer"}},
            "required": ["first-arg", "first_arg"],
        },
        output_schema={"type": "object", "properties": {"ok": {"type": "boolean"}}},
    )
    stub = upstreams.render_catalog_stub([tool])
    compile(stub, "catalog_stub.py", "exec")
    assert "first_arg: str" in stub
    assert "first_arg_2: int" in stub
    script = (
        "import asyncio\n"
        "async def main():\n"
        '    return await collide(first_arg="x", first_arg_2=1)\n'
        "asyncio.run(main())\n"
    )
    snap = monty.Monty(script, type_check=True, type_check_stubs=stub).start(
        print_callback=monty.CollectStreams()
    )
    assert isinstance(snap, monty.FunctionSnapshot)


def test_render_catalog_stub_colliding_result_class_names_disambiguate():
    import pydantic_monty as monty

    # Distinct py_names that PascalCase to the same Result base must emit distinct result classes.
    tool_ab = _tool(
        "a_b",
        input_schema={"type": "object", "properties": {"x": {"type": "string"}}, "required": ["x"]},
        output_schema={"type": "object", "properties": {"url": {"type": "string"}}},
        py_arg_map={"x": "x"},
    )
    tool_a__b = _tool(
        "a__b",
        input_schema={"type": "object", "properties": {"y": {"type": "integer"}}, "required": ["y"]},
        output_schema={"type": "object", "properties": {"count": {"type": "integer"}}},
        py_arg_map={"y": "y"},
    )
    stub = upstreams.render_catalog_stub([tool_ab, tool_a__b])
    compile(stub, "catalog_stub.py", "exec")

    result_classes = re.findall(r"class (\w+Result\d*)\(TypedDict\):", stub)
    assert len(result_classes) == 2
    assert len(set(result_classes)) == 2, f"duplicate result class names: {result_classes}"

    ab_return = re.search(r"def a_b\(.*?\) -> (\w+):", stub).group(1)
    a__b_return = re.search(r"def a__b\(.*?\) -> (\w+):", stub).group(1)
    assert ab_return != a__b_return
    assert ab_return in result_classes and a__b_return in result_classes

    script = (
        "import asyncio\n"
        "async def main():\n"
        '    r = await a_b(x="s")\n'
        '    _ = r["url"]\n'
        "    q = await a__b(y=1)\n"
        '    return q["count"]\n'
        "asyncio.run(main())\n"
    )
    snap = monty.Monty(script, type_check=True, type_check_stubs=stub).start(
        print_callback=monty.CollectStreams()
    )
    assert isinstance(snap, monty.FunctionSnapshot)


async def test_discover_disambiguates_colliding_property_names(home, monkeypatch):
    # py_arg_map must round-trip BOTH colliding real names, not silently drop one.
    real_list_tools = ClientSession.list_tools

    async def patched(self):
        result = await real_list_tools(self)
        for t in result.tools:
            if t.name == "add":
                t.inputSchema = {
                    "type": "object",
                    "properties": {"first-arg": {"type": "integer"}, "first_arg": {"type": "integer"}},
                }
        return result

    monkeypatch.setattr(ClientSession, "list_tools", patched)
    _write_upstreams(home, [_fixture_server_cfg(skip=["boom"])])
    await upstreams.discover_upstreams()
    add = upstreams.get_tool("fixture_add")
    assert add.py_arg_map == {"first_arg": "first-arg", "first_arg_2": "first_arg"}


def test_render_catalog_stub_non_object_input_falls_back_to_kwargs():
    import pydantic_monty as monty

    # No nameable properties but a real constraint → permissive **kwargs signature.
    tool = _tool(
        "freeform",
        input_schema={"type": "object", "additionalProperties": {"type": "string"}},
        output_schema={"type": "object", "properties": {"ok": {"type": "boolean"}}},
    )
    stub = upstreams.render_catalog_stub([tool])
    compile(stub, "catalog_stub.py", "exec")
    assert "**kwargs: Any" in stub
    script = (
        "import asyncio\n"
        "async def main():\n"
        '    r = await freeform(anything="x")\n'
        '    return r["ok"]\n'
        "asyncio.run(main())\n"
    )
    snap = monty.Monty(
        script, type_check=True, type_check_stubs=stub
    ).start(print_callback=monty.CollectStreams())
    assert isinstance(snap, monty.FunctionSnapshot)


async def test_discover_warns_on_unusable_input_schema(home, monkeypatch, caplog):
    real_list_tools = ClientSession.list_tools

    async def patched(self):
        result = await real_list_tools(self)
        for t in result.tools:
            if t.name == "add":
                t.inputSchema = {"type": "object", "additionalProperties": {"type": "string"}}
        return result

    monkeypatch.setattr(ClientSession, "list_tools", patched)
    _write_upstreams(home, [_fixture_server_cfg(skip=["boom"])])
    with caplog.at_level("WARNING"):
        await upstreams.discover_upstreams()
    assert any("no usable top-level 'properties'" in r.message for r in caplog.records)


async def test_discover_builds_arg_map_for_non_identifier_property(home, monkeypatch):
    # py_arg_map maps a sanitized arg back to a non-identifier wire property name.
    real_list_tools = ClientSession.list_tools

    async def patched(self):
        result = await real_list_tools(self)
        for t in result.tools:
            if t.name == "add":
                t.inputSchema = {
                    "type": "object",
                    "properties": {"first-num": {"type": "integer"}},
                    "required": ["first-num"],
                }
        return result

    monkeypatch.setattr(ClientSession, "list_tools", patched)
    _write_upstreams(home, [_fixture_server_cfg(skip=["boom"])])
    await upstreams.discover_upstreams()
    add = upstreams.get_tool("fixture_add")
    assert add.py_arg_map == {"first_num": "first-num"}


def test_infer_shape_names_fields_and_broad_types():
    assert upstreams.infer_shape(
        {"id": "x", "n": 1, "ok": True, "ratio": 1.5, "xs": [1], "sub": {"a": 1}, "nil": None}
    ) == {
        "id": "str",
        "n": "int",
        "ok": "bool",
        "ratio": "float",
        "xs": "list",
        "sub": "dict",
        "nil": "None",
    }


def test_infer_shape_of_a_result_with_no_fields_is_none():
    assert upstreams.infer_shape(None) is None
    assert upstreams.infer_shape("plain text") is None
    assert upstreams.infer_shape([{"id": "x"}]) is None


def test_merge_shapes_unions_fields_and_degrades_conflicts():
    merged = upstreams.merge_shapes({"id": "str"}, {"id": "str", "count": "int"})
    assert merged == {"id": "str", "count": "int"}
    assert upstreams.merge_shapes(merged, {"id": "int"}) == {"id": "unknown", "count": "int"}


def test_merge_shapes_lets_a_null_observation_yield_to_a_real_type():
    assert upstreams.merge_shapes({"f": "None"}, {"f": "str"}) == {"f": "str"}
    assert upstreams.merge_shapes({"f": "str"}, {"f": "None"}) == {"f": "str"}
    assert upstreams.merge_shapes({"f": "None"}, {"f": "None"}) == {"f": "None"}
    assert upstreams.merge_shapes({"f": "str"}, {"f": "int"}) == {"f": "unknown"}
    assert upstreams.merge_shapes({"f": "unknown"}, {"f": "str"}) == {"f": "unknown"}
    assert upstreams.merge_shapes({"f": "unknown"}, {"f": "None"}) == {"f": "unknown"}


def test_record_shape_merges_across_calls_and_persists(home):
    tool = _tool("t", input_schema={}, output_schema=None)
    upstreams.record_shape(tool, {"id": "x"})
    upstreams.record_shape(tool, {"id": "x", "count": 2})
    assert tool.learned_shape == {"id": "str", "count": "int"}
    cache = json.loads((home / "upstreams-shapes.json").read_text())
    assert cache == {"s.t": {"id": "str", "count": "int"}}


def test_record_shape_ignores_results_with_no_shape(home):
    tool = _tool("t", input_schema={}, output_schema=None)
    upstreams.record_shape(tool, None)
    upstreams.record_shape(tool, "plain text")
    assert tool.learned_shape is None
    assert not (home / "upstreams-shapes.json").exists()


def test_a_learned_shape_becomes_the_result_type():
    tool = _tool("t", input_schema={}, output_schema=None)
    tool.learned_shape = {
        "id": "str",
        "count": "int",
        "ratio": "float",
        "ok": "bool",
        "xs": "list",
        "sub": "dict",
        "mixed": "unknown",
        "nil": "None",
    }
    stub = upstreams.render_catalog_stub([tool])
    compile(stub, "catalog_stub.py", "exec")
    assert _result_fields(stub, "t") == [
        "id: str",
        "count: int",
        "ratio: float",
        "ok: bool",
        "xs: list",
        "sub: dict",
        "mixed: Any",
        "nil: Any",
    ]


@pytest.mark.parametrize("shape", [False, None, {}])
def test_a_shape_that_types_nothing_leaves_the_result_untyped(shape):
    tool = _tool("t", input_schema={}, output_schema=None)
    tool.learned_shape = shape
    assert "def t() -> Any:" in upstreams.render_catalog_stub([tool])


async def test_a_learned_field_name_that_is_not_an_identifier_is_reachable():
    tool = _tool("t", input_schema={}, output_schema=None)
    tool.learned_shape = {"next-cursor": "str", "type": "str"}
    stub = upstreams.render_catalog_stub([tool])
    compile(stub, "catalog_stub.py", "exec")
    assert _result_fields(stub, "t") == ["next-cursor: str", "type: str"]

    def script(expr: str) -> str:
        return (
            "import asyncio\n"
            "async def main():\n"
            "    r = await t()\n"
            f"    return {expr}\n"
            "asyncio.run(main())\n"
        )

    for expr in ('r["next-cursor"]', 'r["type"]'):
        step = await monty_start(MontyStartInput(script=script(expr), stubs=stub))
        assert step.error is None
        assert [c.function_name for c in step.calls] == ["t"]

    unseen = await monty_start(
        MontyStartInput(script=script('r["next_cursor"]'), stubs=stub)
    )
    assert "MontyTypingError" in unseen.error


def test_declared_schema_beats_a_learned_shape():
    tool = _tool(
        "declared",
        input_schema={},
        output_schema={"type": "object", "properties": {"sum": {"type": "integer"}}},
    )
    tool.learned_shape = {"other": "str"}
    stub = upstreams.render_catalog_stub([tool])
    assert "sum: int" in stub
    assert "other" not in stub


async def test_learned_shape_survives_restart_and_reaches_the_stub(home):
    (home / "upstreams-shapes.json").write_text(
        json.dumps({"fixture.noout_a": {"id": "str", "count": "int"}})
    )
    _write_upstreams(home, [_fixture_server_cfg()])
    await upstreams.discover_upstreams()
    assert upstreams.get_tool("fixture_noout_a").learned_shape == {"id": "str", "count": "int"}
    stub = upstreams.render_registry_stub()
    compile(stub, "catalog_stub.py", "exec")
    assert _result_fields(stub, "fixture_noout_a") == ["id: str", "count: int"]


async def test_call_tool_activity_learns_from_a_real_result(home):
    _write_upstreams(home, [_fixture_server_cfg()])
    await upstreams.discover_upstreams()
    result = await call_tool_activity(
        CallToolRequest(name="fixture_noout_a", arguments={}, session_id="")
    )
    assert result.ok is True
    assert upstreams.get_tool("fixture_noout_a").learned_shape == {"id": "str", "count": "int"}


async def test_call_tool_activity_learns_nothing_from_an_error(home):
    _write_upstreams(home, [_fixture_server_cfg()])
    await upstreams.discover_upstreams()
    result = await call_tool_activity(
        CallToolRequest(name="fixture_boom", arguments={}, session_id="")
    )
    assert result.ok is False
    assert upstreams.get_tool("fixture_boom").learned_shape is None
    assert not (home / "upstreams-shapes.json").exists()


def _raise_permission_error(*args, **kwargs):
    raise PermissionError("home is read-only")


@pytest.mark.parametrize("failing", ["_write_shapes", "_load_shapes"])
async def test_a_failing_shape_cache_does_not_fail_the_call(home, monkeypatch, caplog, failing):
    _write_upstreams(home, [_fixture_server_cfg()])
    await upstreams.discover_upstreams()
    monkeypatch.setattr(upstreams, failing, _raise_permission_error)
    with caplog.at_level("WARNING"):
        result = await call_tool_activity(
            CallToolRequest(name="fixture_noout_a", arguments={}, session_id="")
        )
    assert result.ok is True
    assert result.result == {"id": "a", "count": 1}
    assert "fixture.noout_a" in caplog.text
    assert "PermissionError" in caplog.text


@pytest.mark.parametrize("content", ["", "{not json", "[]", '"x"', "null", "3", '{"s.t": ["a"]}'])
async def test_an_unusable_shape_cache_degrades_without_sinking_discovery(home, caplog, content):
    (home / "upstreams-shapes.json").write_text(content)
    _write_upstreams(home, [_fixture_server_cfg()])
    with caplog.at_level("WARNING"):
        await upstreams.discover_upstreams()
    for py_name in ("fixture_add", "fixture_boom", "fixture_noout_a", "fixture_noout_b"):
        assert upstreams.get_tool(py_name) is not None
    compile(upstreams.render_registry_stub(), "catalog_stub.py", "exec")
    assert str(upstreams.SHAPES_PATH) in caplog.text


@pytest.mark.parametrize("bad", [["a"], {"f": 3}])
async def test_a_malformed_cache_entry_is_dropped_and_a_good_one_survives(home, caplog, bad):
    (home / "upstreams-shapes.json").write_text(
        json.dumps({"fixture.noout_a": {"id": "str"}, "fixture.noout_b": bad})
    )
    _write_upstreams(home, [_fixture_server_cfg()])
    with caplog.at_level("WARNING"):
        await upstreams.discover_upstreams()
    assert upstreams.get_tool("fixture_noout_a").learned_shape == {"id": "str"}
    assert upstreams.get_tool("fixture_noout_b").learned_shape is None
    compile(upstreams.render_registry_stub(), "catalog_stub.py", "exec")
    assert "fixture.noout_b" in caplog.text
    assert str(upstreams.SHAPES_PATH) in caplog.text


def test_an_absent_shape_cache_is_silent(home, caplog):
    with caplog.at_level("WARNING"):
        assert upstreams._load_shapes() == {}
    assert str(upstreams.SHAPES_PATH) not in caplog.text


def test_many_data_derived_keys_discard_the_shape_entirely(home, caplog):
    tool = _tool("t", input_schema={}, output_schema=None)
    with caplog.at_level("WARNING"):
        for i in range(100):
            upstreams.record_shape(tool, {f"user{i}@example.com": "x"})
    stub = upstreams.render_catalog_stub([tool])
    cache = (home / "upstreams-shapes.json").read_text()
    for key in ("user0@example.com", "user99@example.com"):
        assert key not in cache
        assert key not in stub
    assert "def t() -> Any:" in stub
    assert "s.t" in caplog.text


def test_one_result_wider_than_the_cap_discards_the_shape_entirely(home, caplog):
    tool = _tool("t", input_schema={}, output_schema=None)
    with caplog.at_level("WARNING"):
        upstreams.record_shape(tool, {f"user{i}@example.com": "x" for i in range(100)})
    stub = upstreams.render_catalog_stub([tool])
    cache = (home / "upstreams-shapes.json").read_text()
    for key in ("user0@example.com", "user99@example.com"):
        assert key not in cache
        assert key not in stub
    assert "def t() -> Any:" in stub
    assert "s.t" in caplog.text


async def test_the_cap_decision_survives_a_restart(home):
    _write_upstreams(home, [_fixture_server_cfg()])
    await upstreams.discover_upstreams()
    tool = upstreams.get_tool("fixture_noout_a")
    for i in range(100):
        upstreams.record_shape(tool, {f"user{i}@example.com": "x"})

    upstreams._shapes_cache = None
    await upstreams.discover_upstreams()
    reloaded = upstreams.get_tool("fixture_noout_a")
    upstreams.record_shape(reloaded, {"fresh@example.com": "x"})
    stub = upstreams.render_registry_stub()
    assert "def fixture_noout_a() -> Any:" in stub
    assert "fresh@example.com" not in stub
    assert "fresh@example.com" not in (home / "upstreams-shapes.json").read_text()


def test_a_narrow_tool_is_unaffected_by_the_cap(home):
    tool = _tool("t", input_schema={}, output_schema=None)
    upstreams.record_shape(tool, {"id": "x"})
    upstreams.record_shape(tool, {"id": "x", "count": 2})
    assert tool.learned_shape == {"id": "str", "count": "int"}
    assert json.loads((home / "upstreams-shapes.json").read_text()) == {
        "s.t": {"id": "str", "count": "int"}
    }
    stub = upstreams.render_catalog_stub([tool])
    assert _result_fields(stub, "t") == ["id: str", "count: int"]


def test_a_successful_write_leaves_no_temp_file(home):
    tool = _tool("t", input_schema={}, output_schema=None)
    upstreams.record_shape(tool, {"id": "x"})
    path = home / "upstreams-shapes.json"
    assert path.exists()
    assert path.stat().st_mode & 0o777 == 0o600
    assert [p.name for p in home.iterdir()] == ["upstreams-shapes.json"]


def test_a_failing_write_leaves_no_temp_file(home, monkeypatch, caplog):
    monkeypatch.setattr(upstreams.json, "dump", _raise_permission_error)
    tool = _tool("t", input_schema={}, output_schema=None)
    with caplog.at_level("WARNING"):
        upstreams.record_shape(tool, {"id": "x"})
    assert list(home.iterdir()) == []


def _noout_script(expr: str) -> str:
    return (
        "import asyncio\n"
        "async def main():\n"
        "    r = await fixture_noout_a()\n"
        f"    return {expr}\n"
        "asyncio.run(main())\n"
    )


async def test_a_learned_shape_types_the_result_and_an_unseen_field_is_rejected(home):
    _write_upstreams(home, [_fixture_server_cfg()])
    await upstreams.discover_upstreams()
    call = await call_tool_activity(
        CallToolRequest(name="fixture_noout_a", arguments={}, session_id="")
    )
    assert call.ok is True
    stub = upstreams.render_registry_stub()
    assert _result_fields(stub, "fixture_noout_a") == ["id: str", "count: int"]

    seen = await monty_start(MontyStartInput(script=_noout_script('r["id"]'), stubs=stub))
    assert seen.error is None
    assert [c.function_name for c in seen.calls] == ["fixture_noout_a"]

    unseen = await monty_start(
        MontyStartInput(script=_noout_script('r["never_seen"]'), stubs=stub)
    )
    assert "MontyTypingError" in unseen.error

    escaped = await monty_start(
        MontyStartInput(script=_noout_script('r.get("never_seen")'), stubs=stub)
    )
    assert escaped.error is None
    assert [c.function_name for c in escaped.calls] == ["fixture_noout_a"]


async def test_a_recorded_shape_round_trips_through_the_cache(home):
    _write_upstreams(home, [_fixture_server_cfg()])
    await upstreams.discover_upstreams()
    await call_tool_activity(
        CallToolRequest(name="fixture_noout_a", arguments={}, session_id="")
    )
    recorded = upstreams.get_tool("fixture_noout_a").learned_shape
    assert recorded == {"id": "str", "count": "int"}

    upstreams._shapes_cache = None
    await upstreams.discover_upstreams()
    assert upstreams.get_tool("fixture_noout_a").learned_shape == recorded
    stub = upstreams.render_registry_stub()
    assert _result_fields(stub, "fixture_noout_a") == ["id: str", "count: int"]
