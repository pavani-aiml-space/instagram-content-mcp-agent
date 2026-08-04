"""
MCP Client Helper

Spawns mcp_server/instagram_tools_server.py as a subprocess over stdio,
opens a real MCP ClientSession against it, and loads its tools as
LangChain BaseTool objects via langchain-mcp-adapters.

Must be run with the project root as the working directory (same
requirement as backend/main.py's absolute imports).
"""

import json
import os
import sys
import uuid
from contextlib import asynccontextmanager
from typing import Any

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from langchain_core.messages import ToolMessage
from langchain_core.tools import BaseTool
from langchain_mcp_adapters.tools import load_mcp_tools

_SERVER_PARAMS = StdioServerParameters(
    command=sys.executable,
    args=["-m", "mcp_server.instagram_tools_server"],
    env=os.environ.copy(),
)


@asynccontextmanager
async def mcp_tools_session():
    """
    Async context manager yielding {tool_name: BaseTool} loaded from the
    Instagram tools MCP server. The server subprocess and session stay
    open for the lifetime of the `with` block - use one session per
    coordinator run rather than spawning a server per tool call.
    """
    async with stdio_client(_SERVER_PARAMS) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = await load_mcp_tools(session)
            yield {tool.name: tool for tool in tools}


async def call_mcp_tool(tool: BaseTool, args: dict[str, Any]) -> dict:
    """
    Call an MCP-loaded LangChain tool and return the dict our FastMCP tool
    function actually returned.

    Invokes with a full ToolCall (not a bare args dict) so LangChain returns
    a ToolMessage whose `.artifact["structured_content"]` is the
    schema-validated dict FastMCP already computed server-side - every tool
    in mcp_server/instagram_tools_server.py is annotated `-> dict`, so FastMCP
    populates CallToolResult.structuredContent for free, and
    langchain-mcp-adapters loads tools with response_format="content_and_artifact"
    to carry it through. Falls back to parsing the text content block for any
    tool that doesn't return structured content.
    """
    result = await tool.ainvoke({
        "name": tool.name,
        "args": args,
        "id": str(uuid.uuid4()),
        "type": "tool_call",
    })

    if isinstance(result, ToolMessage) and result.artifact and "structured_content" in result.artifact:
        return result.artifact["structured_content"]

    content = result.content if isinstance(result, ToolMessage) else result
    if isinstance(content, list) and content and isinstance(content[0], dict) and "text" in content[0]:
        return json.loads(content[0]["text"])
    raise ValueError(f"Unexpected MCP tool result shape: {result!r}")
