"""
Image Generator Agent
Generates images from caption, topic, and content
"""

from typing import List, Optional

from langchain_core.tools import BaseTool
from agents.mcp_client import call_mcp_tool


def _build_image_prompt(base_topic: str, caption: str, topic_details: str) -> str:
    """
    Build a simple image prompt from caption, topic, and content.
    Prioritizes caption as the main description.
    """
    caption = (caption or "").strip()
    topic_details = (topic_details or "").strip()

    # Priority: Use caption if available (it's the most descriptive)
    if caption:
        prompt = caption
        # Only add topic details if they provide additional context not in caption
        if topic_details and topic_details.lower() not in caption.lower():
            prompt = f"{prompt}, {topic_details}"
    elif base_topic:
        prompt = base_topic
        if topic_details:
            prompt = f"{prompt}, {topic_details}"
    else:
        prompt = "A professional, Instagram-worthy image"

    return prompt


async def run_image_generator(
    prompt: str,
    tool: BaseTool,
    aspect_ratio: str = "1:1",
    caption: str = "",
    bullets: Optional[List[str]] = None,
    topic_details: str = ""
) -> dict:
    """
    Run the Image Generator Agent - calls the "generate_image" tool loaded
    from the Instagram Tools MCP server (see agents/mcp_client.py).

    Args:
        prompt: Core image idea or topic
        tool: The "generate_image" MCP tool (loaded via agents/mcp_client.py)
        aspect_ratio: Image aspect ratio (default 1:1 for IG feed)
        caption: Optional caption text
        bullets: Optional list of key points
        topic_details: Optional extra context

    Returns:
        Dictionary with image_url, is_placeholder, status, error
    """
    image_prompt = _build_image_prompt(prompt, caption, topic_details)

    try:
        result = await call_mcp_tool(tool, {
            "prompt": image_prompt,
            "aspect_ratio": aspect_ratio,
            "caption": caption,
            "bullets": bullets or [],
            "topic_details": topic_details,
        })
    except Exception as e:
        return {"image_url": "", "status": "error", "error": f"Image generation failed: {str(e)}"}

    if result.get("status") == "error":
        return {"image_url": "", "status": "error", "error": result.get("error", "Image generation failed")}

    return {
        "image_url": result["image_url"],
        "is_placeholder": result.get("is_placeholder", False),
        "status": "completed",
        "error": "",
    }
