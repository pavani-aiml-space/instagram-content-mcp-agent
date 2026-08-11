"""
Instagram Poster Agent
Specialized agent for posting content to Instagram
"""

from langchain_core.tools import BaseTool
from agents.mcp_client import call_mcp_tool


async def run_instagram_poster(
    image_url: str,
    caption: str,
    instagram_account_id: str,
    tool: BaseTool,
    dry_run: bool = False,
    format: str = "post",
) -> dict:
    """
    Run the Instagram Poster Agent - calls the "post_to_instagram" tool
    loaded from the Instagram Tools MCP server (see agents/mcp_client.py).

    Args:
        image_url: Image URL to post
        caption: Caption text
        instagram_account_id: Instagram Business Account ID
        tool: The "post_to_instagram" MCP tool (loaded via agents/mcp_client.py)
        dry_run: If True, validates/logs without publishing to the real account
        format: "post" or "story" (mapped to the Graph API's media_type field
            server-side; "reel" is rejected since this pipeline only produces
            a static image, not a video)

    Returns:
        Dictionary with post_id, permalink, status, error
    """
    try:
        result = await call_mcp_tool(tool, {
            "image_url": image_url,
            "caption": caption,
            "instagram_account_id": instagram_account_id,
            "dry_run": dry_run,
            "format": format,
        })
    except Exception as e:
        return {"post_id": "", "permalink": "", "status": "error", "error": f"Instagram posting failed: {str(e)}"}

    if result.get("status") == "error":
        return {"post_id": "", "permalink": "", "status": "error", "error": result.get("error", "Instagram posting failed")}

    return {"post_id": result["post_id"], "permalink": result.get("permalink", ""), "status": "completed", "error": ""}
