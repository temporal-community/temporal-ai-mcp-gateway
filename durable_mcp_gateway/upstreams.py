"""Upstream MCP config loading, discovery, and the runtime call path.

This is the seam between the durable backend and the real MCP servers it proxies. Discovery
populates a module-level registry keyed by a sanitized Python identifier (``py_name``); the
call path looks a tool up by ``py_name`` and forwards to the real ``tool_name``.

Connect-per-operation: every discovery and every tool call opens a brand-new session and
tears it down — no pooling. Sessions are cheap relative to a durable Activity and pooling
across the Activity boundary would be fragile.

A tool's result type comes from its own declared ``outputSchema`` when it has one, else from
the SHAPE its past results taught us. Every successful call, to any tool, teaches that shape —
field names and broad types, never the values, though a result keyed by data stores those keys
as field names, which is what ``_MAX_LEARNED_FIELDS`` bounds — merged across calls and cached
in ``upstreams-shapes.json`` so it survives a restart. A tool with no declared schema returns
the TypedDict rendered from its learned shape; a tool with neither registers with an unknown
return. A learned shape is a union over the calls seen so far and so is necessarily incomplete:
indexing a field it does not carry is a type error before the script runs, and ``.get()`` is
the way to reach one.
"""

import asyncio
import json
import keyword
import logging
import os
import re
import tempfile
from contextlib import AsyncExitStack, asynccontextmanager
from dataclasses import dataclass
from typing import Any, Literal

from mcp import ClientSession, StdioServerParameters
from mcp.client.auth import OAuthClientProvider, TokenStorage
from mcp.client.stdio import stdio_client
from mcp.client.streamable_http import streamablehttp_client
from mcp.shared.auth import OAuthClientMetadata

# NOTE: no top-level `from . import config` — this module is loaded standalone (no package
# context) by a test, so package-relative imports must stay function-local (see below),
# matching how HOME_DIR is read straight from os.environ rather than via config.

logger = logging.getLogger(__name__)


class ReconnectRequired(RuntimeError):
    """Raised when an OAuth upstream has no usable token (never connected, or a full
    re-auth would be needed). The user must (re)run connect."""


def find_reconnect(exc: BaseException) -> "ReconnectRequired | None":
    """Return a ReconnectRequired nested anywhere in ``exc`` (incl. ExceptionGroups), else None.

    The MCP streamable-http client runs the OAuth flow inside an anyio task group, so a
    ReconnectRequired raised by the no-browser handlers surfaces wrapped in an
    ExceptionGroup. Callers use this to detect "needs authorization" through that wrapping.
    """
    if isinstance(exc, ReconnectRequired):
        return exc
    if isinstance(exc, BaseExceptionGroup):
        for sub in exc.exceptions:
            found = find_reconnect(sub)
            if found is not None:
                return found
    return None

# Base dir for all config/state. Mirrors how config.DB_PATH derives ~/.durable-mcp-gateway/,
# but overridable on its own so tests can redirect the whole dir without touching DB_PATH.
HOME_DIR = os.environ.get(
    "DURABLE_MCP_GATEWAY_HOME",
    os.path.join(os.path.expanduser("~"), ".durable-mcp-gateway"),
)
UPSTREAMS_PATH = os.path.join(HOME_DIR, "upstreams.json")
SHAPES_PATH = os.path.join(HOME_DIR, "upstreams-shapes.json")

_VALID_TRANSPORTS = ("stdio", "streamable-http")
# Per-upstream connect+list ceiling. A wedged upstream degrades (warn + skip), not hangs.
_DISCOVER_TIMEOUT = 15.0


class UpstreamConfigError(RuntimeError):
    """Raised when upstreams.json is structurally invalid (bad transport, missing fields)."""


@dataclass
class UpstreamTool:
    namespaced_name: str
    server_name: str
    tool_name: str
    description: str
    input_schema: dict
    output_schema: dict | None
    server_cfg: dict
    py_name: str
    # sanitized arg name -> real input-schema property name
    py_arg_map: dict[str, str]
    # field name -> broad type, merged from real results; False once the field cap was
    # crossed, which stops learning for this tool for good (see record_shape)
    learned_shape: dict[str, str] | Literal[False] | None = None


@dataclass
class DiscoveryReport:
    """Outcome of a discovery pass, so callers can decide how strict to be.

    ``discover_upstreams`` degrades on a per-upstream connect failure (warn + skip) rather
    than raising, because the backend must not let one flaky upstream block startup. But that
    swallows information a strict pre-flight check (``validate``) needs. So the outcome is
    reported here instead of discarded: ``connected`` maps each upstream that came up to its
    tool count; ``failed`` lists the upstreams that could not be connected, with the reason.
    The backend ignores ``failed`` (degrade); ``validate`` treats it as a failure.
    """

    connected: dict[str, int]
    failed: list[tuple[str, str]]


_REGISTRY: dict[str, UpstreamTool] = {}


def get_tool(py_name: str) -> UpstreamTool | None:
    """Return the registered :class:`UpstreamTool` for a sanitized ``py_name``, or None."""
    return _REGISTRY.get(py_name)


_NON_IDENTIFIER = re.compile(r"[^A-Za-z0-9_]+")


def sanitize_identifier(s: str) -> str:
    """Turn an arbitrary tool/arg name into a valid Python identifier."""
    out = _NON_IDENTIFIER.sub("_", s)
    if out and out[0].isdigit():
        out = "_" + out
    if not out or keyword.iskeyword(out) or keyword.issoftkeyword(out):
        out = out + "_"
    return out


def sanitize_unique(names: Any) -> dict[str, str]:
    """Map each raw name to a unique sanitized identifier, disambiguating collisions deterministically."""
    result: dict[str, str] = {}
    used: set[str] = set()
    for raw in names:
        base = sanitize_identifier(raw)
        candidate = base
        n = 1
        while candidate in used:
            n += 1
            candidate = f"{base}_{n}"
        used.add(candidate)
        result[raw] = candidate
    return result


def _has_nontrivial_schema(schema: dict) -> bool:
    """Whether an input schema constrains arguments despite having no top-level ``properties``."""
    if not schema:
        return False
    if schema.get("type") not in (None, "object"):
        return True
    return any(
        k in schema
        for k in ("additionalProperties", "$ref", "allOf", "anyOf", "oneOf")
    )


_UNRESOLVED_VAR = re.compile(r"\$(\{[^}]*\}|[A-Za-z_][A-Za-z0-9_]*)")


def expand_env(value: Any) -> Any:
    """Recursively expand ``${VAR}`` / ``$VAR`` references in strings inside config values.

    Raises if an expanded string still contains an unresolved ``${VAR}`` or ``$VAR`` — an
    unresolved variable is a misconfiguration we surface loudly rather than passing a literal
    ``${VAR}`` to a server. ``os.path.expandvars`` leaves an unset ``$VAR`` (no braces)
    literal, so the leftover-reference check must catch the brace-less form too.
    """
    if isinstance(value, str):
        expanded = os.path.expandvars(value)
        if _UNRESOLVED_VAR.search(expanded):
            raise RuntimeError(
                f"unresolved environment variable in config value: {value!r}"
            )
        return expanded
    if isinstance(value, dict):
        return {k: expand_env(v) for k, v in value.items()}
    if isinstance(value, list):
        return [expand_env(v) for v in value]
    return value


def load_servers() -> list[dict]:
    """Parse ``upstreams.json`` into a validated list of server config dicts.

    Absent file → empty list + a WARNING (running with no upstreams is valid). Each entry is
    validated for ``name`` and a supported ``transport`` with its required transport field.
    """
    if not os.path.exists(UPSTREAMS_PATH):
        logger.warning(
            "no upstreams config at %s; running with no upstream tools", UPSTREAMS_PATH
        )
        return []
    with open(UPSTREAMS_PATH) as f:
        cfg = json.load(f)
    servers = cfg.get("servers", [])
    if not isinstance(servers, list):
        raise UpstreamConfigError('upstreams.json "servers" must be a list')

    for s in servers:
        name = s.get("name")
        if not name:
            raise UpstreamConfigError(f'upstream entry missing "name": {s!r}')
        transport = s.get("transport")
        if transport not in _VALID_TRANSPORTS:
            raise UpstreamConfigError(
                f"upstream {name!r}: transport must be one of {_VALID_TRANSPORTS}, "
                f"got {transport!r}"
            )
        if transport == "stdio" and not s.get("command"):
            raise UpstreamConfigError(f'upstream {name!r}: stdio transport requires "command"')
        if transport == "streamable-http" and not s.get("url"):
            raise UpstreamConfigError(f'upstream {name!r}: streamable-http transport requires "url"')
    # Expand ``${VAR}``/``$VAR`` across every value eagerly here — at load time, before the
    # degrade-tolerant discovery loop — so an unresolved variable aborts loading loudly
    # instead of being swallowed as a per-upstream "failed to connect" warning.
    return [expand_env(s) for s in servers]


_UNKNOWN_FIELD_TYPE = "unknown"
_NULL_FIELD_TYPE = "None"
# A record has a bounded set of fields; an object keyed by data (ids, emails, filenames)
# does not. Crossing this width is the signal that the keys are values, not a schema.
_MAX_LEARNED_FIELDS = 64
_shapes_cache: dict[str, dict[str, str] | Literal[False]] | None = None


def _broad_type(value: Any) -> str:
    if isinstance(value, bool):
        return "bool"
    if isinstance(value, int):
        return "int"
    if isinstance(value, float):
        return "float"
    if isinstance(value, str):
        return "str"
    if isinstance(value, list):
        return "list"
    if isinstance(value, dict):
        return "dict"
    return _NULL_FIELD_TYPE


def infer_shape(value: Any) -> dict[str, str] | None:
    """Return one result's field names and broad types, or None if it carries no shape.

    Only the name and kind of each top-level field — never a value. A result that isn't a
    JSON object has no shape to learn, including the ``None`` that a text block which isn't
    JSON normalizes to.
    """
    if not isinstance(value, dict):
        return None
    return {k: _broad_type(v) for k, v in value.items()}


def merge_shapes(old: dict[str, str], new: dict[str, str]) -> dict[str, str]:
    """Union two observations: a field seen in either is in the shape, and a field whose
    type differs between them degrades to ``unknown`` — except that a ``None`` observation
    is not a conflict, since a nullable field still has its type when it has a value."""
    merged = dict(old)
    for field, kind in new.items():
        seen = merged.get(field, kind)
        if seen == kind or kind == _NULL_FIELD_TYPE:
            merged[field] = seen
        elif seen == _NULL_FIELD_TYPE:
            merged[field] = kind
        else:
            merged[field] = _UNKNOWN_FIELD_TYPE
    return merged


def _is_shape_entry(value: Any) -> bool:
    if value is False:
        return True
    return isinstance(value, dict) and all(
        isinstance(v, str) for v in value.values()
    )


def _read_shapes_file() -> dict[str, dict[str, str] | Literal[False]]:
    if not os.path.exists(SHAPES_PATH):
        return {}
    try:
        with open(SHAPES_PATH) as f:
            raw = json.load(f)
    except (OSError, ValueError) as e:
        logger.warning("ignoring unreadable shape cache %s: %r", SHAPES_PATH, e)
        return {}
    if not isinstance(raw, dict):
        logger.warning(
            "ignoring shape cache %s: expected a JSON object, got %s",
            SHAPES_PATH,
            type(raw).__name__,
        )
        return {}
    shapes = {k: v for k, v in raw.items() if _is_shape_entry(v)}
    malformed = sorted(k for k in raw if k not in shapes)
    if malformed:
        logger.warning(
            "dropping malformed entries from shape cache %s: %s",
            SHAPES_PATH,
            ", ".join(malformed),
        )
    return shapes


def _load_shapes() -> dict[str, dict[str, str] | Literal[False]]:
    """The whole learned-shape cache, keyed by namespaced name, read from disk once."""
    global _shapes_cache
    if _shapes_cache is None:
        _shapes_cache = _read_shapes_file()
    return _shapes_cache


def _write_shapes(shapes: dict[str, dict[str, str] | Literal[False]]) -> None:
    """Persist the cache: 0600 + atomic replace, like vault.FileCredentialStore.

    Whole-blob like the vault too, so two backends writing at once can drop each other's
    newly learned fields. The loss is sticky: a backend rewrites only when its own merged
    shape changes, so a field it already holds in memory is not written back by the next call.
    """
    os.makedirs(HOME_DIR, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=HOME_DIR, prefix="upstreams-shapes-", suffix=".tmp")
    try:
        with os.fdopen(fd, "w") as f:
            json.dump(shapes, f)
        os.replace(tmp, SHAPES_PATH)
    except BaseException:
        os.unlink(tmp)
        raise


def record_shape(tool: UpstreamTool, result: Any) -> None:
    """Merge one real result's shape into ``tool`` and persist it, if it taught us anything.

    Mutates the registered :class:`UpstreamTool` in place, so the next rendered stub carries
    the shape with no restart. Disk is touched only when the merged shape actually changed.
    A tool whose merged shape crosses ``_MAX_LEARNED_FIELDS`` has that shape discarded and is
    never learned from again — persisted as ``False``, so the stop survives a restart.
    """
    try:
        if tool.learned_shape is False:
            return
        shape = infer_shape(result)
        if shape is None:
            return
        merged: dict[str, str] | Literal[False] = merge_shapes(
            tool.learned_shape or {}, shape
        )
        if len(merged) > _MAX_LEARNED_FIELDS:
            logger.warning(
                "tool %r returned more than %d distinct result fields; discarding its "
                "learned shape and no longer learning from it",
                tool.namespaced_name,
                _MAX_LEARNED_FIELDS,
            )
            merged = False
        elif merged == tool.learned_shape:
            return
        tool.learned_shape = merged
        shapes = _load_shapes()
        shapes[tool.namespaced_name] = merged
        _write_shapes(shapes)
    except Exception as e:  # noqa: BLE001
        # The shape cache is advisory; the upstream call already succeeded and its result
        # must reach the caller even if we cannot record what it looked like.
        logger.warning(
            "could not record the result shape for %r: %r", tool.namespaced_name, e
        )


def is_oauth(server_cfg: dict) -> bool:
    """Whether this upstream uses brokered OAuth (auth.type == "oauth")."""
    return (server_cfg.get("auth") or {}).get("type") == "oauth"


def _warn_unsupported_auth(server_cfg: dict) -> None:
    """Warn (once per server) if an auth flow we don't implement is configured.

    Static/bearer header auth is handled via ``headers``; ``oauth`` is handled by the
    vault-backed provider. Anything else is accepted for forward-compat but not performed.
    """
    kind = (server_cfg.get("auth") or {}).get("type")
    if kind not in (None, "bearer", "oauth"):
        logger.warning(
            "upstream %r: auth.type=%r is not yet supported; proceeding without it "
            "(configure static 'headers' instead)",
            server_cfg.get("name"),
            kind,
        )


def oauth_client_metadata(server_cfg: dict) -> OAuthClientMetadata:
    """The client metadata the gateway/CLI present to an OAuth upstream.

    Shared by the connect path (CLI) and the call path (activity) so the dynamically
    registered client — stored in the vault and reused — is identical either way.
    """
    from . import config  # function-local: keep this module standalone-loadable

    return OAuthClientMetadata(
        redirect_uris=[config.OAUTH_REDIRECT_URI],  # type: ignore[list-item]
        token_endpoint_auth_method="none",
        grant_types=["authorization_code", "refresh_token"],
        response_types=["code"],
        scope=(server_cfg.get("auth") or {}).get("scope"),
        client_name="durable-mcp-gateway",
    )


def _oauth_provider(
    server_cfg: dict, token_storage: TokenStorage
) -> OAuthClientProvider:
    """Build an OAuthClientProvider backed by the vaulted token for this (user, upstream).

    The call path never opens a browser: if the provider finds no valid token and would
    need a full re-auth, the no-browser handlers raise :class:`ReconnectRequired`, which the
    caller turns into a clear "run connect again" tool error. Token refresh (and rotation
    write-back) happens transparently through ``token_storage``.
    """
    name = server_cfg.get("name")

    async def _no_browser(_auth_url: str) -> None:
        raise ReconnectRequired(
            f"upstream {name!r} needs (re)authorization — run the connect flow again"
        )

    async def _no_callback() -> tuple[str, str | None]:
        raise ReconnectRequired(
            f"upstream {name!r} needs (re)authorization — run the connect flow again"
        )

    provider = OAuthClientProvider(
        server_url=server_cfg["url"],
        client_metadata=oauth_client_metadata(server_cfg),
        storage=token_storage,
        redirect_handler=_no_browser,
        callback_handler=_no_callback,
    )

    # Re-prime the provider's in-memory expiry from the vault's stored absolute expires_at.
    # The SDK never restores expiry on load, so without this a freshly-built provider deems a
    # loaded-but-expired token "valid", skips the refresh, sends the dead token, gets a 401,
    # and its 401 path does a *full re-auth* (-> ReconnectRequired) instead of refreshing.
    # Priming it makes is_token_valid() honest so the working proactive-refresh path fires.
    # _initialize() (which loads the token on first request) leaves token_expiry_time alone,
    # so setting it now survives; after a successful refresh the SDK updates it itself.
    stored_expiry = getattr(token_storage, "stored_expiry", None)
    if stored_expiry is not None:
        provider.context.token_expiry_time = stored_expiry()
    return provider


@asynccontextmanager
async def upstream_session(server_cfg: dict, token_storage: TokenStorage | None = None):
    """Open and initialize a fresh MCP ClientSession to one upstream, then tear it down.

    stdio or streamable-http per ``transport``. The config is already env-expanded at load
    time. For ``auth.type == "oauth"`` the caller must pass the vault-backed ``token_storage``
    for the relevant (user, upstream); the session authenticates via an OAuthClientProvider
    that refreshes transparently. Otherwise streamable-http uses static ``headers`` only.
    """
    transport = server_cfg.get("transport")
    async with AsyncExitStack() as stack:
        if transport == "stdio":
            params = StdioServerParameters(
                command=server_cfg["command"],
                args=server_cfg.get("args", []) or [],
                env=server_cfg.get("env") or None,
            )
            read, write = await stack.enter_async_context(stdio_client(params))
        elif transport == "streamable-http":
            _warn_unsupported_auth(server_cfg)
            if is_oauth(server_cfg):
                if token_storage is None:
                    raise ReconnectRequired(
                        f"upstream {server_cfg.get('name')!r} uses OAuth but no token is "
                        "available — run the connect flow first"
                    )
                read, write, _ = await stack.enter_async_context(
                    streamablehttp_client(
                        server_cfg["url"], auth=_oauth_provider(server_cfg, token_storage)
                    )
                )
            else:
                headers = server_cfg.get("headers") or None
                read, write, _ = await stack.enter_async_context(
                    streamablehttp_client(server_cfg["url"], headers=headers)
                )
        else:
            raise UpstreamConfigError(f"unsupported MCP transport: {transport!r}")
        session = await stack.enter_async_context(ClientSession(read, write))
        await session.initialize()
        yield session


async def _discover_one(server_cfg: dict, token_storage: TokenStorage | None = None) -> None:
    """Connect to one upstream, list its tools, and register every non-skipped one.

    For an OAuth upstream, ``token_storage`` carries the user's vaulted token so listing
    authenticates; without it (not yet connected) ``upstream_session`` raises ReconnectRequired.
    """
    name = server_cfg["name"]
    skip = set(server_cfg.get("skip") or [])
    async with upstream_session(server_cfg, token_storage) as session:
        listing = await session.list_tools()
    for t in listing.tools:
        if t.name in skip:
            continue
        namespaced = f"{name}.{t.name}"
        py_name = sanitize_identifier(namespaced)
        if py_name in _REGISTRY:
            logger.warning(
                "duplicate tool %r (sanitized name %r already registered); skipping the duplicate",
                namespaced,
                py_name,
            )
            continue
        output_schema = dict(t.outputSchema) if getattr(t, "outputSchema", None) else None
        input_schema = dict(t.inputSchema or {})
        properties = input_schema.get("properties") or {}
        if not properties and _has_nontrivial_schema(input_schema):
            logger.warning(
                "tool %r input schema has no usable top-level 'properties'; exposing a "
                "permissive (**kwargs) signature so it stays callable",
                namespaced,
            )
        py_arg_map = {san: raw for raw, san in sanitize_unique(properties).items()}
        _REGISTRY[py_name] = UpstreamTool(
            namespaced_name=namespaced,
            server_name=name,
            tool_name=t.name,
            description=t.description or "",
            input_schema=input_schema,
            output_schema=output_schema,
            server_cfg=server_cfg,
            py_name=py_name,
            py_arg_map=py_arg_map,
            learned_shape=_load_shapes().get(namespaced),
        )


async def discover_upstreams() -> DiscoveryReport:
    """Connect to every configured upstream and populate the registry.

    Degrades on a per-upstream *connect failure/timeout* (warn + continue — a transient
    outage of one upstream must not sink the rest) and records it in the returned
    :class:`DiscoveryReport` so a strict caller (``validate``) can still fail on it. But a
    configured OAuth upstream that isn't authorized is a misconfiguration, not an outage:
    those are collected and cause a hard RuntimeError after the loop, telling you to run the
    connect CLI.
    """
    from . import config, vault as vault_mod  # function-local: keep this module standalone-loadable

    _REGISTRY.clear()
    vault = None
    unauthorized: list[str] = []
    failed: list[tuple[str, str]] = []
    connected: dict[str, int] = {}
    for server_cfg in load_servers():
        name = server_cfg["name"]
        # OAuth upstreams list with the local user's vaulted token; if it isn't connected
        # (or a full re-auth is needed), _discover_one raises ReconnectRequired.
        # OAuth listing goes through the same provider as the call path, so an
        # expired-but-refreshable token is refreshed (and written back) right here at
        # discovery — not only on the first tool call. A missing / unrefreshable token
        # raises ReconnectRequired (hard-fail below). NOTE: discovery is thus a second
        # refresh site and shares the single-flight caveat (see call_tool_activity's
        # oauth-refresh TODO and vault.py's limitations) — a boot discovery and a
        # concurrent tool call can both refresh the same (user, upstream).
        token_storage = None
        if is_oauth(server_cfg):
            if vault is None:
                vault = vault_mod.open_default_vault()
            token_storage = vault.storage_for(config.LOCAL_USER_ID, name)
        try:
            await asyncio.wait_for(
                _discover_one(server_cfg, token_storage), timeout=_DISCOVER_TIMEOUT
            )
        except Exception as e:  # noqa: BLE001 - one bad upstream must not sink the rest
            if find_reconnect(e) is not None:
                # Not an outage — the operator must authorize this upstream. Fail hard below.
                unauthorized.append(name)
            else:
                logger.warning("failed to connect upstream %r: %r; skipping", name, e)
                failed.append((name, str(e)))
            continue
        count = sum(1 for t in _REGISTRY.values() if t.server_name == name)
        connected[name] = count
        logger.info("connected upstream %r: %d tool(s)", name, count)

    if unauthorized:
        raise RuntimeError(
            "these OAuth upstreams are configured but not authorized:\n  - "
            + "\n  - ".join(unauthorized)
            + "\n\nAuthorize each before starting the backend:\n"
            + "\n".join(f"    {config.CONNECT_HINT} {n}" for n in unauthorized)
        )

    return DiscoveryReport(connected=connected, failed=failed)


def join_text_blocks(content: Any) -> str:
    """Concatenate the ``text`` payloads of every TextContent block in ``content``."""
    parts: list[str] = []
    for block in content or []:
        block_type = getattr(block, "type", None)
        if block_type is None and isinstance(block, dict):
            block_type = block.get("type")
        if block_type != "text":
            continue
        text = getattr(block, "text", None)
        if text is None and isinstance(block, dict):
            text = block.get("text")
        if text:
            parts.append(text)
    return "\n".join(parts)


def structured_or_json(result: Any) -> Any:
    """Prefer the MCP result's ``structuredContent``; else parse its first text block as JSON."""
    sc = getattr(result, "structuredContent", None)
    if sc is not None:
        return sc
    text = join_text_blocks(getattr(result, "content", None))
    if text:
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            pass
    return None


def is_error(result: Any) -> bool:
    """Whether an MCP CallToolResult signaled ``isError``."""
    return bool(getattr(result, "isError", False))


# Max nesting depth before falling back to ``dict``.
_MAX_STUB_DEPTH = 3

_SCALAR_TYPES = {
    "string": "str",
    "integer": "int",
    "number": "float",
    "boolean": "bool",
}

# Broad types from _broad_type that already name a Python type. The rest — a field whose type
# conflicted across calls, or one only ever seen null — carry no usable type.
_LEARNED_FIELD_TYPES = frozenset({"bool", "int", "float", "str", "list", "dict"})


def _to_class_name(py_name: str) -> str:
    """Name a generated TypedDict by PascalCasing a sanitized ``py_name``."""
    return "".join(part.capitalize() for part in py_name.split("_") if part)


class _StubBuilder:
    """Renders one JSON-Schema-typed catalog into a Python stub string."""

    def __init__(self) -> None:
        self.typed_dicts: list[str] = []
        self._counter = 0

    def _fresh_name(self, base: str) -> str:
        self._counter += 1
        return f"{base}{self._counter}"

    def _map_type(self, schema: Any, td_base: str, depth: int) -> str:
        if not isinstance(schema, dict):
            return "Any"
        kind = schema.get("type")
        if isinstance(kind, list):
            kind = next((k for k in kind if k != "null"), None)
        if kind in _SCALAR_TYPES:
            return _SCALAR_TYPES[kind]
        if kind == "array":
            items = schema.get("items")
            inner = self._map_type(items, td_base, depth) if items else "Any"
            return f"list[{inner}]"
        if kind == "object":
            props = schema.get("properties")
            if not props or depth >= _MAX_STUB_DEPTH:
                return "dict"
            return self._emit_typed_dict(self._fresh_name(td_base), schema, depth + 1)
        return "Any"

    def _emit_typed_dict(self, class_name: str, schema: dict, depth: int) -> str:
        props = schema.get("properties") or {}
        field_names = sanitize_unique(props)
        lines = [f"class {class_name}(TypedDict):"]
        if not props:
            lines.append("    pass")
        for prop, prop_schema in props.items():
            field = field_names[prop]
            field_type = self._map_type(prop_schema, f"{class_name}Field", depth)
            lines.append(f"    {field}: {field_type}")
        self.typed_dicts.append("\n".join(lines))
        return class_name

    def _emit_learned_typed_dict(self, class_name: str, shape: dict[str, str]) -> str:
        # Functional form, not the class form: a learned field name is a raw result key,
        # which need not be an identifier ("next-cursor") and may be a keyword ("type").
        # Sanitizing it into an attribute would declare a key the result does not have.
        fields = ", ".join(
            f"{field!r}: {kind if kind in _LEARNED_FIELD_TYPES else 'Any'}"
            for field, kind in shape.items()
        )
        self.typed_dicts.append(f'{class_name} = TypedDict("{class_name}", {{{fields}}})')
        return class_name

    def _result_type(self, tool: UpstreamTool) -> str:
        # _fresh_name disambiguates py_names that PascalCase to the same Result base.
        base = _to_class_name(tool.py_name) + "Result"
        if tool.output_schema is None:
            # A TypedDict with no fields rejects every key, so an empty (or abandoned)
            # shape types nothing.
            if not tool.learned_shape:
                return "Any"
            return self._emit_learned_typed_dict(self._fresh_name(base), tool.learned_shape)
        schema = tool.output_schema
        if schema.get("type") == "object":
            return self._emit_typed_dict(self._fresh_name(base), schema, 1)
        return self._map_type(schema, base, 0)

    def _function(self, tool: UpstreamTool) -> str:
        result_type = self._result_type(tool)
        props = tool.input_schema.get("properties") or {}
        required = set(tool.input_schema.get("required") or [])
        arg_names = sanitize_unique(props)
        params: list[str] = []
        for prop, prop_schema in props.items():
            arg = arg_names[prop]
            arg_type = self._map_type(prop_schema, f"{_to_class_name(tool.py_name)}Arg", 0)
            if prop in required:
                params.append(f"{arg}: {arg_type}")
            else:
                params.append(f"{arg}: {arg_type} = ...")
        if params:
            # Keyword-only so dispatch always sees kwargs to reverse-map via py_arg_map.
            sig = "*, " + ", ".join(params)
        elif _has_nontrivial_schema(tool.input_schema):
            # No nameable properties but the schema constrains inputs — stay callable.
            sig = "**kwargs: Any"
        else:
            sig = ""
        # Tool functions are async: the sandbox awaits them (and can asyncio.gather several to
        # run them concurrently). The type checker enforces the await — a missing one is a
        # not-subscriptable / unused-awaitable error on the returned coroutine.
        lines = [f"async def {tool.py_name}({sig}) -> {result_type}:"]
        doc = tool.description.strip()
        if tool.output_schema is None and tool.learned_shape:
            observed = (
                "This tool declares no output schema: its result type carries the fields past "
                "calls returned, merged across them, so it is neither complete nor guaranteed "
                "for any one call. Indexing a field it does not list is a type error — reach "
                'one with result.get("field"), and check a listed field is present before '
                "using it. That type does not guarantee the result is a dict on any given "
                "call — it may be a list, a string, a number, or None for a plain-text "
                "result — so check before indexing."
            )
            doc = f"{doc}\n\n    {observed}" if doc else observed
        if doc:
            escaped = doc.replace("\\", "\\\\").replace('"""', '\\"\\"\\"')
            lines.append(f'    """{escaped}"""')
        lines.append("    ...")
        return "\n".join(lines)

    def render(self, tools: list[UpstreamTool]) -> str:
        functions = [self._function(t) for t in tools]
        blocks = ["from typing import Any, TypedDict"]
        blocks.extend(self.typed_dicts)
        blocks.extend(functions)
        return "\n\n\n".join(blocks) + "\n"


def render_catalog_stub(tools: list[UpstreamTool]) -> str:
    """Render a typed Python stub describing every tool as a keyword-only function (TypedDict results, not dataclasses — the host returns a plain dict, and a dataclass result type-checks but crashes at runtime)."""
    return _StubBuilder().render(tools)


def render_registry_stub() -> str:
    """Render the catalog stub for the currently-discovered registry."""
    return render_catalog_stub(list(_REGISTRY.values()))


def render_registry_catalog() -> list[dict]:
    """Render the JSON catalog (one entry per tool) for the currently-discovered registry."""
    return [
        {
            "name": t.namespaced_name,
            "py_name": t.py_name,
            "py_arg_map": t.py_arg_map,
            "description": t.description,
            "input_schema": t.input_schema,
            "output_schema": t.output_schema,
        }
        for t in _REGISTRY.values()
    ]


async def setup_worker() -> DiscoveryReport:
    """Shared Worker bootstrap: discover upstreams (populate the registry).

    Both the backend (:mod:`.serve`) and the debug harness host ``call_tool_activity``, so
    both call this before building their Worker; the registry is served to the stdio server over
    Temporal rather than written to disk — only each tool's learned shape is cached, seeded
    from ``upstreams-shapes.json`` here and written back as calls teach it more. Returns the
    :class:`DiscoveryReport` so ``validate`` can fail on a connect failure the backend
    deliberately degrades past.
    """
    return await discover_upstreams()
