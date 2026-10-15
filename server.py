
import os
import hashlib


EMAIL = "23f2001486@ds.study.iitm.ac.in"

from mcp.server.fastmcp import FastMCP, Context
from mcp.server.transport_security import TransportSecuritySettings

mcp = FastMCP(
    "ExamChallenge",
    stateless_http=True,
    json_response=True,
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
    headers = {
        key.lower(): value
        for key, value in (ctx.headers or {}).items()
    }

    challenge = headers.get("x-exam-challenge")

    if challenge is None:
        raise ValueError("Missing X-Exam-Challenge header")

    email = EMAIL.strip().lower()
    text = f"{challenge}:{email}"

    return hashlib.sha256(
        text.encode("utf-8")
    ).hexdigest()[:16]


if __name__ == "__main__":
    mcp.settings.host = "0.0.0.0"
    mcp.settings.port = int(os.environ.get("PORT", "10000"))
    mcp.run(transport="streamable-http")
