"""A tiny stdio MCP server used by the upstream-discovery tests.

Tools: ``add`` returns structured content (a typed result, so it carries an outputSchema),
``boom`` always errors (the upstream returns ``isError``), and ``noout_a`` / ``noout_b`` opt
out of structured output so FastMCP synthesizes no ``outputSchema`` — they exercise the
unknown-return path. ``noout_a`` returns a JSON object as text (a shape to learn),
``noout_b`` plain text (nothing to learn). Run over stdio so the tests need no network.
"""

import json

from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel

mcp = FastMCP("fixture")


class AddResult(BaseModel):
    sum: int


@mcp.tool()
def add(a: int, b: int) -> AddResult:
    return AddResult(sum=a + b)


@mcp.tool()
def boom() -> str:
    raise ValueError("intentional failure")


@mcp.tool(structured_output=False)
def noout_a() -> str:
    return json.dumps({"id": "a", "count": 1})


@mcp.tool(structured_output=False)
def noout_b() -> str:
    return "b"


if __name__ == "__main__":
    mcp.run(transport="stdio")
