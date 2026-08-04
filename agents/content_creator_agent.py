"""
Content Creator Agent
Specialized agent for generating Instagram content (captions + hashtags)
"""

from langchain_core.tools import BaseTool
from agents.mcp_client import call_mcp_tool


async def run_content_creator(topic: str, tool: BaseTool, format: str = "post", topic_details: str = "") -> dict:
    """
    Run the Content Creator Agent - calls the "generate_content" tool loaded
    from the Instagram Tools MCP server (see agents/mcp_client.py).

    Args:
        topic: Content topic
        tool: The "generate_content" MCP tool (loaded via agents/mcp_client.py)
        format: Content format
        topic_details: Optional additional details/context about the topic

    Returns:
        Dictionary with caption, bullets, hashtags, status, error
    """
    try:
        result = await call_mcp_tool(tool, {
            "topic": topic,
            "format": format,
            "topic_details": topic_details,
        })
    except Exception as e:
        return {"caption": "", "bullets": [], "hashtags": "", "status": "error", "error": f"Content generation failed: {str(e)}"}

    if result.get("status") == "error":
        return {"caption": "", "bullets": [], "hashtags": "", "status": "error", "error": result.get("error", "Content generation failed")}

    return {
        "caption": result["caption"],
        "bullets": result.get("bullets", []),
        "hashtags": result["hashtags"],
        "status": "completed",
        "error": "",
    }
