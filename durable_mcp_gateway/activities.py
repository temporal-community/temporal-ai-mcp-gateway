"""The host-call Activity backing the sandbox's per-tool host functions.

``call_tool_activity`` looks a tool up in the upstream registry by its sanitized ``py_name``,
validates the arguments, and forwards the call to the real ``tool_name`` over a fresh session.

No ``from __future__ import annotations`` — CallToolRequest/CallToolResult cross Temporal's
pydantic converter, and stringized annotations trip its TypeAdapter build.
"""

import re

import jsonschema
from jsonschema import Draft202012Validator
from temporalio import activity

from . import upstreams, vault as vault_mod
from .models import Catalog, CallToolRequest, CallToolResult


class RetryableUpstreamError(RuntimeError):
    """A transient-looking upstream failure (rate limit, 5xx, dropped connection).

    Raised from ``call_tool_activity`` so Temporal retries the Activity with backoff; a
    genuine tool error (bad args, not-found, logical failure) is returned as
    ``CallToolResult(ok=False)`` instead, which does NOT retry. Upstreams like Notion throttle
    intermittently (HTTP 429), so a couple of automatic retries usually get through where a
    single direct call would just fail — the durability win of running tool calls as
    Activities. Generic across MCPs: classification is on HTTP status / common phrasing.
    """


# Transient HTTP statuses worth retrying (429 rate limit, 408/425 timeouts, 5xx server).
_RETRYABLE_STATUS = {"408", "425", "429", "500", "502", "503", "504"}
# Match a 3-digit status only in HTTP-ish context ("status": 429, code 503, http 502) so we
# don't retry on an innocent "500" that happens to appear in a tool's error text.
_STATUS_CTX_RE = re.compile(r"(?:status|statuscode|code|http)[^\d]{0,8}(\d{3})", re.IGNORECASE)
_RETRYABLE_PHRASES = (
    "rate limit", "rate_limited", "too many requests",
    "temporarily unavailable", "service unavailable", "bad gateway",
    "gateway timeout", "overloaded", "timed out", "read timeout",
    "connection reset", "connection aborted", "server disconnected",
    "remote protocol error",
    # A connection that never came up is as transient as one that broke mid-flight. httpx
    # raises the whole establishment family — DNS failure, refused, unreachable, TLS
    # handshake — as ConnectError/ConnectTimeout, and PoolTimeout when no connection comes
    # free; the "(" anchors those to a flattened exception repr, so a tool's own prose can't
    # match. The errno phrases below catch the same failures raised bare (socket.gaierror,
    # OSError from a stdio upstream), whose wording is per-platform.
    "connecterror(", "connecttimeout(", "pooltimeout(", "gaierror(",
    "connection refused", "network is unreachable", "no route to host",
    "nodename nor servname", "name or service not known",
    "temporary failure in name resolution",
)


def _is_retryable_upstream_error(text: str) -> bool:
    """True if ``text`` looks like a transient upstream failure worth a Temporal retry."""
    t = text or ""
    for m in _STATUS_CTX_RE.finditer(t):
        if m.group(1) in _RETRYABLE_STATUS:
            return True
    low = t.lower()
    return any(p in low for p in _RETRYABLE_PHRASES)


def _exc_text(exc: BaseException) -> str:
    """Flatten an exception (incl. ExceptionGroup members) into one searchable string."""
    parts = [repr(exc)]
    if isinstance(exc, BaseExceptionGroup):
        for sub in exc.exceptions:
            parts.append(_exc_text(sub))
    return " | ".join(parts)


@activity.defn
async def get_catalog_stub() -> str:
    """Return the typed stub for the currently-discovered registry."""
    return upstreams.render_registry_stub()


@activity.defn
async def get_catalog() -> Catalog:
    """Return both the typed stub and the raw JSON catalog for the currently-discovered registry."""
    return Catalog(
        stub=upstreams.render_registry_stub(),
        tools=upstreams.render_registry_catalog(),
    )


@activity.defn
async def call_tool_activity(request: CallToolRequest) -> CallToolResult:
    """Run one upstream MCP tool call durably and return its result envelope."""
    tool = upstreams.get_tool(request.name)
    if tool is None:
        return CallToolResult(ok=False, error=f"unknown tool {request.name!r}")

    # For an OAuth upstream, resolve the session handle to a user and hand the call
    # the vault-backed token storage for that (user, upstream). The vault is opened
    # fresh per call (cheap) so a token the gateway refreshed/wrote is always current.
    #
    # TODO(oauth-refresh): token refresh is NOT single-flighted. The OAuthClientProvider
    # below refreshes on expiry/401 and set_tokens persists the rotated pair, but two
    # concurrent activities (or a Temporal retry) for the same (user, upstream) with an
    # expired token will both spend the same refresh token -> the loser gets
    # invalid_grant (and some IdPs revoke the whole grant on replay). Port the
    # oauth-local RefreshCoordinator (per-(user, upstream) lock) for the in-process case,
    # and back it with a distributed lock across workers -- a Postgres advisory lock once
    # the vault moves to a DB, or a RefreshWorkflow keyed refresh:{user}:{upstream}
    # (workflow-id uniqueness as the mutex). See vault.py's known-limitations note.
    token_storage = None
    if upstreams.is_oauth(tool.server_cfg):
        vault = vault_mod.open_default_vault()
        try:
            user_id = vault.user_for_session(request.session_id)
        except KeyError:
            return CallToolResult(
                ok=False,
                error=(
                    f"no authenticated session for OAuth upstream {tool.server_name!r}; "
                    "run the connect flow first"
                ),
            )
        token_storage = vault.storage_for(user_id, tool.server_name)

    # Map sanitized kwargs back to the real input-schema property names.
    arguments = {
        tool.py_arg_map.get(k, k): v for k, v in request.arguments.items()
    }

    try:
        # Pin the draft explicitly: an MCP inputSchema often omits ``$schema``, and letting
        # jsonschema infer the draft would let validation semantics shift implicitly.
        # check_schema raises SchemaError on an unusable schema (validate() alone would not).
        Draft202012Validator.check_schema(tool.input_schema)
        Draft202012Validator(tool.input_schema).validate(arguments)
    except jsonschema.ValidationError as e:
        return CallToolResult(
            ok=False,
            error=f"arguments did not match schema for {request.name!r}: {e.message}",
        )
    except jsonschema.SchemaError as e:
        # An unusable schema is the tool's problem, not the caller's — don't block the call.
        activity.logger.warning(
            "input schema for %r is invalid (%s); skipping validation", request.name, e
        )

    try:
        async with upstreams.upstream_session(tool.server_cfg, token_storage) as session:
            result = await session.call_tool(tool.tool_name, arguments)
    except Exception as e:  # noqa: BLE001
        # "Needs authorization" is data, not an activity failure — return it as a clean
        # tool error (no Temporal retry). The signal may be wrapped in an ExceptionGroup
        # by the MCP client's task group, so unwrap.
        reconnect = upstreams.find_reconnect(e)
        if reconnect is not None:
            return CallToolResult(ok=False, error=str(reconnect))
        # The --no-temporal runner calls this outside any Activity, so there is no Worker to stop.
        details = activity.cancellation_details() if activity.in_activity() else None
        if details is not None and details.worker_shutdown:
            # The Worker is stopping, which tears this session down mid-call — the tool
            # didn't fail. Fail the Activity so Temporal reruns the call on the next Worker
            # instead of handing the script a bogus error.
            raise
        text = _exc_text(e)
        # A transient connection error (reset/timeout/etc.) is worth a durable retry.
        if _is_retryable_upstream_error(text):
            raise RetryableUpstreamError(text) from e
        # Anything else is a real, non-transient failure — surface it to the script as a
        # catchable tool error rather than failing/retrying the whole activity.
        return CallToolResult(ok=False, error=text)
    if upstreams.is_error(result):
        error = upstreams.join_text_blocks(getattr(result, "content", None))
        if not error:
            # No text blocks (the upstream returned only structured content) — fall back to a
            # repr of the structured value so the error message isn't empty.
            error = str(upstreams.structured_or_json(result))
        # A rate limit / 5xx comes back as an MCP error *result* (not an exception); raise it
        # so Temporal retries with backoff. Genuine tool errors stay ok=False (no retry).
        if _is_retryable_upstream_error(error):
            raise RetryableUpstreamError(error)
        return CallToolResult(ok=False, error=error)
    value = upstreams.structured_or_json(result)
    upstreams.record_shape(tool, value)
    return CallToolResult(ok=True, result=value)


ALL_ACTIVITIES = [call_tool_activity, get_catalog_stub, get_catalog]
