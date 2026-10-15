
import os
import hashlib

from mcp.server.fastmcp import FastMCP, Context

EMAIL = "23f2001486@ds.study.iitm.ac.in"

mcp = FastMCP(
    "ExamChallenge",
    stateless_http=True,
    json_response=True
)


@mcp.tool()
def solve_challenge(ctx: Context) -> str:
    """Solve the exam challenge using the current HTTP request header."""

    headers = ctx.headers or {}
    challenge = headers.get("x-exam-challenge")

    if not challenge:
        raise ValueError("Missing X-Exam-Challenge header")

    text = f"{challenge}:{EMAIL}"
    answer = hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]

    return answer


if __name__ == "__main__":
    mcp.settings.host = "0.0.0.0"
    mcp.settings.port = int(os.environ.get("PORT", "10000"))
    mcp.run(transport="streamable-http")
