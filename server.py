
import os
import hashlib

from mcp.server.fastmcp import FastMCP, Context
from mcp.server.transport_security import TransportSecuritySettings

EMAIL = "23f2001486@ds.study.iitm.ac.in".strip().lower()

mcp = FastMCP(
    "ExamChallenge",
    stateless_http=True,
    transport_security=TransportSecuritySettings(
        allowed_hosts=[
            "mcpserver-iedu.onrender.com",
            "mcpserver-iedu.onrender.com:*",
        ],
        allowed_origins=[
            "https://mcpserver-iedu.onrender.com",
        ],
    ),
)


@mcp.tool()
def solve_challenge(ctx: Context) -> str:
    """Return the hash for the challenge in the current HTTP request."""

    # First try the original HTTP request's headers.
    request_context = ctx.request_context
    request = getattr(request_context, "request", None)

    if request is not None:
        headers = request.headers
    else:
        headers = ctx.headers or {}

    challenge = headers.get("x-exam-challenge")

    if challenge is None:
        raise ValueError("Missing X-Exam-Challenge header")

    text = f"{challenge}:{EMAIL}"
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]


if __name__ == "__main__":
    mcp.settings.host = "0.0.0.0"
    mcp.settings.port = int(os.environ.get("PORT", "10000"))
    mcp.run(transport="streamable-http")
