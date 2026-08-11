"""
Instagram Tools MCP Server

A real Model Context Protocol server (stdio transport) exposing three tools:
  - generate_content    -> tools/content_generator.py (LangChain ChatOpenAI + structured output)
  - generate_image      -> tools/image_generator.py
  - post_to_instagram   -> tools/instagram_poster.py (Instagram Graph API, supports dry_run)

These wrap the existing tool classes directly - no logic is duplicated here,
only the MCP protocol boundary (JSON-RPC over stdio) is added.

Run standalone for inspection:
    mcp dev mcp_server/instagram_tools_server.py

Run as a server (spawned by agents/mcp_client.py):
    python -m mcp_server.instagram_tools_server
"""

import os
from typing import Any, Optional

from mcp.server.fastmcp import FastMCP

from tools.content_generator import ContentGenerator
from tools.image_generator import ImageGenerator
from tools.instagram_poster import InstagramPoster

mcp = FastMCP("instagram-tools")


@mcp.tool()
def generate_content(topic: str, format: str = "post", topic_details: Optional[str] = None) -> dict[str, Any]:
    """
    Generate an Instagram caption, bullet points, and hashtags for a topic.

    Args:
        topic: Content topic (e.g. "LLM", "AI Agents", "Pumpkin Pie")
        format: Content format - "post", "story", or "reel"
        topic_details: Optional additional details/context about the topic

    Returns:
        dict with "caption", "bullets", "hashtags" on success, or "status"/"error" on failure.
    """
    try:
        generator = ContentGenerator()
        result = generator.generate(topic=topic, format=format, topic_details=topic_details)
        return {**result, "status": "success"}
    except Exception as e:
        return {"status": "error", "error": str(e)}


@mcp.tool()
def generate_image(
    prompt: str,
    aspect_ratio: str = "1:1",
    caption: Optional[str] = None,
    bullets: Optional[list[str]] = None,
    topic_details: Optional[str] = None,
) -> dict[str, Any]:
    """
    Generate an Instagram-ready image from a text prompt.

    Args:
        prompt: Text description of the image (high-level concept)
        aspect_ratio: "1:1", "4:5", "16:9", or "9:16"
        caption: Optional caption text (used only to enrich the prompt, not overlaid on the image)
        bullets: Optional list of bullet points (used only to enrich the prompt)
        topic_details: Optional additional details/context about the topic

    Returns:
        dict with "image_url" on success, or "status"/"error" on failure.
    """
    try:
        generator = ImageGenerator()
        result = generator.generate(
            prompt=prompt,
            aspect_ratio=aspect_ratio,
            caption=caption,
            bullets=bullets,
            topic_details=topic_details,
        )
        return {
            "image_url": result["image_url"],
            "is_placeholder": result.get("is_placeholder", False),
            "status": "success",
        }
    except Exception as e:
        return {"status": "error", "error": str(e)}


# Maps the app's "format" concept to the Graph API's actual "media_type" field.
# None means "omit media_type", which the Graph API treats as a plain feed post.
_FORMAT_TO_MEDIA_TYPE = {
    "post": None,
    "story": "STORIES",
}


@mcp.tool()
def post_to_instagram(
    image_url: str,
    caption: str,
    instagram_account_id: str,
    dry_run: bool = False,
    format: str = "post",
) -> dict[str, Any]:
    """
    Post an image with a caption to Instagram using the Graph API.

    Args:
        image_url: Publicly accessible URL of the image to post
        caption: Caption text (can include hashtags)
        instagram_account_id: Instagram Business Account ID
        dry_run: If True, validates inputs and logs what would be posted without
            publishing to the real Instagram account. A DRY_RUN env var set to
            "true"/"1"/"yes" forces this on regardless of the request, as a
            deployment-wide safety net.
        format: "post" (default) or "story". Mapped to the Graph API's media_type
            field: "post" omits media_type (a plain feed post), "story" sends
            media_type=STORIES. "reel" is rejected: the Graph API requires a
            REELS container to carry a video_url, and this pipeline only ever
            generates a static image, so there is no video to post - accepting
            "reel" here would silently publish a plain feed image under the
            Reel label instead.

    Returns:
        dict with "post_id" and "permalink" on success, or "status"/"error" on failure.
    """
    effective_dry_run = dry_run or os.getenv("DRY_RUN", "false").lower() in ("1", "true", "yes")

    normalized_format = (format or "post").lower()
    if normalized_format == "reel":
        return {
            "status": "error",
            "error": (
                "format='reel' is not supported: Instagram Reels require a video "
                "(media_type=REELS with a video_url), and this pipeline only "
                "generates a static image. Use 'post' or 'story' instead."
            ),
        }
    if normalized_format not in _FORMAT_TO_MEDIA_TYPE:
        return {
            "status": "error",
            "error": f"Unknown format '{format}'. Expected 'post' or 'story'.",
        }
    media_type = _FORMAT_TO_MEDIA_TYPE[normalized_format]

    try:
        poster = InstagramPoster()
        result = poster.post_image(
            image_url=image_url,
            caption=caption,
            instagram_account_id=instagram_account_id,
            dry_run=effective_dry_run,
            media_type=media_type,
        )
        return {
            "post_id": result["post_id"],
            "permalink": result.get("permalink", ""),
            "status": result.get("status", "success"),
        }
    except Exception as e:
        return {"status": "error", "error": str(e)}


if __name__ == "__main__":
    mcp.run(transport="stdio")
