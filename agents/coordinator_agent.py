"""
Coordinator Agent
Orchestrates multiple specialized agents to create and post Instagram content

This is the main orchestrator that:
1. Opens one MCP session against the Instagram Tools server (agents/mcp_client.py)
2. Calls Content Creator Agent
3. Calls Image Generator Agent
4. Calls Instagram Poster Agent

Built with LangChain Expression Language (LCEL) rather than LangGraph: the
flow is strictly linear (content -> image -> post, no branching, no cycles),
so a `RunnableSequence` (the `|` pipe operator) expresses it directly without
graph machinery. Each step also gets `.with_retry()` - a real LCEL benefit
over the previous version, which had no retry behavior at all - so a
transient failure calling OpenAI, Stability, or the Instagram Graph API gets
one automatic retry before it's recorded as a failed step.
"""

import logging
from typing import TypedDict, Annotated, List, Dict, Optional
from langchain_core.runnables import RunnableLambda
from langchain_core.tools import BaseTool
from agents.mcp_client import mcp_tools_session
from agents.content_creator_agent import run_content_creator
from agents.image_generator_agent import run_image_generator
from agents.instagram_poster_agent import run_instagram_poster

# Set up logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Retries are capped at 2 attempts (1 retry) since each attempt is a real,
# billed call to an external API (OpenAI / Stability / Instagram) - enough
# to absorb a transient blip without silently tripling API spend on a
# genuinely broken request.
RETRY_KWARGS = {"stop_after_attempt": 2, "wait_exponential_jitter": True}


class CoordinatorState(TypedDict):
    """State for Coordinator Agent - orchestrates all agents"""
    topic: Annotated[str, "Content topic"]
    topic_details: Annotated[str, "Additional details/context about the topic"]
    format: Annotated[str, "Content format (post/story/reel)"]
    user_id: Annotated[str, "User ID"]
    instagram_account_id: Annotated[str, "Instagram Business Account ID"]
    dry_run: Annotated[bool, "If true, validate/log the Instagram post without publishing"]

    # Content Creator Agent results
    caption: Annotated[str, "Generated caption"]
    bullets: Annotated[List[str], "Generated bullet points"]
    hashtags: Annotated[str, "Generated hashtags"]

    # Image Generator Agent results
    image_url: Annotated[str, "Generated image URL"]

    # Instagram Poster Agent results
    post_id: Annotated[str, "Instagram post ID"]
    permalink: Annotated[str, "Post permalink"]

    # Workflow status
    status: Annotated[str, "Current status"]
    error: Annotated[str, "Error message if any"]
    current_step: Annotated[str, "Current step in workflow"]
    progress_log: Annotated[List[Dict[str, str]], "Progress log entries"]


def create_coordinator_chain(tools: Dict[str, BaseTool]):
    """
    Create the main coordinator chain (an LCEL RunnableSequence)

    `tools` is the {tool_name: BaseTool} dict loaded from the Instagram
    Tools MCP server for this run (see agents/mcp_client.py). Each step
    below calls into one of the specialized agents, passing the matching
    MCP-derived tool through, and retries once on failure before giving up.

    Chain: content_creator | image_generator | instagram_poster
    """

    async def _attempt_content_creator(state: CoordinatorState) -> CoordinatorState:
        result = await run_content_creator(
            topic=state["topic"],
            tool=tools["generate_content"],
            format=state.get("format", "post"),
            topic_details=state.get("topic_details", "")
        )
        if result["status"] == "error":
            raise RuntimeError(result.get("error", "Content creation failed"))

        state["caption"] = result["caption"]
        state["bullets"] = result.get("bullets", [])
        state["hashtags"] = result["hashtags"]
        state["status"] = "content_created"
        logger.info(f"✅ Step 1/3: Content Creator Agent completed - Caption: {len(result['caption'])} chars, Bullets: {len(result.get('bullets', []))}, Hashtags: {len(result['hashtags'])} chars")
        state["progress_log"].append({
            "step": "1",
            "agent": "Content Creator",
            "status": "completed",
            "message": f"Generated caption ({len(result['caption'])} chars), {len(result.get('bullets', []))} bullets, and hashtags"
        })
        return state

    content_creator_with_retry = RunnableLambda(_attempt_content_creator).with_retry(**RETRY_KWARGS)

    async def call_content_creator_node(state: CoordinatorState) -> CoordinatorState:
        """Step 1: Call Content Creator Agent"""
        state["current_step"] = "content_creation"
        state["status"] = "generating_content"

        logger.info(f"📝 Step 1/3: Starting Content Creator Agent for topic: {state['topic']}")
        state["progress_log"].append({
            "step": "1",
            "agent": "Content Creator",
            "status": "starting",
            "message": f"Generating content for topic: {state['topic']}"
        })

        try:
            return await content_creator_with_retry.ainvoke(state)
        except Exception as e:
            error_msg = f"Content creation failed: {str(e)}"
            logger.error(f"❌ Content Creator Agent failed after retry: {error_msg}")
            state["error"] = error_msg
            state["status"] = "error"
            state["progress_log"].append({
                "step": "1",
                "agent": "Content Creator",
                "status": "error",
                "message": error_msg
            })
            return state

    async def _attempt_image_generator(state: CoordinatorState) -> CoordinatorState:
        # Pass topic directly - image generator will build prompt from caption, topic, and content
        result = await run_image_generator(
            prompt=state['topic'],
            tool=tools["generate_image"],
            aspect_ratio="1:1",
            caption=state.get("caption", ""),
            bullets=state.get("bullets", []),
            topic_details=state.get("topic_details", "")
        )
        if result["status"] == "error":
            raise RuntimeError(result.get("error", "Image generation failed"))

        state["image_url"] = result["image_url"]
        state["status"] = "image_generated"
        if result.get("is_placeholder"):
            logger.warning(f"⚠️ Step 2/3: Image Generator used a placeholder image (generation failed) - {result['image_url']}")
            step_2_message = "Image generation failed - used a placeholder image so the post can still go out"
        else:
            logger.info(f"✅ Step 2/3: Image Generator Agent completed - Image URL: {result['image_url']}")
            step_2_message = f"Generated image: {result['image_url'][:50]}..."
        state["progress_log"].append({
            "step": "2",
            "agent": "Image Generator",
            "status": "completed",
            "message": step_2_message
        })
        return state

    image_generator_with_retry = RunnableLambda(_attempt_image_generator).with_retry(**RETRY_KWARGS)

    async def call_image_generator_node(state: CoordinatorState) -> CoordinatorState:
        """Step 2: Call Image Generator Agent"""
        state["current_step"] = "image_generation"
        state["status"] = "generating_image"

        logger.info(f"🎨 Step 2/3: Starting Image Generator Agent for topic: {state['topic']}")
        state["progress_log"].append({
            "step": "2",
            "agent": "Image Generator",
            "status": "starting",
            "message": f"Generating image for topic: {state['topic']}"
        })

        try:
            return await image_generator_with_retry.ainvoke(state)
        except Exception as e:
            error_msg = f"Image generation failed: {str(e)}"
            logger.error(f"❌ Image Generator Agent failed after retry: {error_msg}")
            state["error"] = error_msg
            state["status"] = "error"
            state["progress_log"].append({
                "step": "2",
                "agent": "Image Generator",
                "status": "error",
                "message": error_msg
            })
            return state

    async def _attempt_instagram_poster(state: CoordinatorState) -> CoordinatorState:
        full_caption = f"{state['caption']}\n\n{state['hashtags']}"

        result = await run_instagram_poster(
            image_url=state["image_url"],
            caption=full_caption,
            instagram_account_id=state["instagram_account_id"],
            tool=tools["post_to_instagram"],
            dry_run=state.get("dry_run", False),
            format=state.get("format", "post"),
        )
        if result["status"] == "error":
            raise RuntimeError(result.get("error", "Instagram posting failed"))

        state["post_id"] = result["post_id"]
        state["permalink"] = result.get("permalink", "")
        state["status"] = "posted"
        logger.info(f"✅ Step 3/3: Instagram Poster Agent completed - Post ID: {result['post_id']}")
        state["progress_log"].append({
            "step": "3",
            "agent": "Instagram Poster",
            "status": "completed",
            "message": f"Posted to Instagram! Post ID: {result['post_id']}"
        })
        return state

    instagram_poster_with_retry = RunnableLambda(_attempt_instagram_poster).with_retry(**RETRY_KWARGS)

    async def call_instagram_poster_node(state: CoordinatorState) -> CoordinatorState:
        """Step 3: Call Instagram Poster Agent"""
        state["current_step"] = "instagram_posting"
        state["status"] = "posting_to_instagram"

        logger.info(f"📤 Step 3/3: Starting Instagram Poster Agent")
        state["progress_log"].append({
            "step": "3",
            "agent": "Instagram Poster",
            "status": "starting",
            "message": "Posting content to Instagram"
        })

        try:
            return await instagram_poster_with_retry.ainvoke(state)
        except Exception as e:
            error_msg = f"Instagram posting failed: {str(e)}"
            logger.error(f"❌ Instagram Poster Agent failed after retry: {error_msg}")
            state["error"] = error_msg
            state["status"] = "error"
            state["progress_log"].append({
                "step": "3",
                "agent": "Instagram Poster",
                "status": "error",
                "message": error_msg
            })
            return state

    # LCEL RunnableSequence: content -> image -> post
    return (
        RunnableLambda(call_content_creator_node)
        | RunnableLambda(call_image_generator_node)
        | RunnableLambda(call_instagram_poster_node)
    )


async def run_coordinator(
    topic: str,
    format: str,
    user_id: str,
    instagram_account_id: str,
    topic_details: Optional[str] = None,
    dry_run: bool = False,
) -> dict:
    """
    Run the Coordinator Agent to orchestrate the full pipeline

    Opens one MCP session against the Instagram Tools server for the whole
    run (spawns the server as a subprocess, loads its 3 tools once) rather
    than reconnecting per step.

    Args:
        topic: Content topic
        format: Content format
        user_id: User ID
        instagram_account_id: Instagram Business Account ID
        topic_details: Optional additional details/context about the topic
        dry_run: If True, the Instagram Poster Agent validates/logs the post
            without publishing it to the real account

    Returns:
        Dictionary with all results from all agents
    """
    logger.info(f"🚀 Starting Coordinator Agent pipeline - Topic: {topic}, Format: {format}")
    if topic_details:
        logger.info(f"📝 Topic details: {topic_details[:100]}...")

    initial_state: CoordinatorState = {
        "topic": topic,
        "topic_details": topic_details or "",
        "format": format,
        "user_id": user_id,
        "instagram_account_id": instagram_account_id,
        "dry_run": dry_run,
        "caption": "",
        "bullets": [],
        "hashtags": "",
        "image_url": "",
        "post_id": "",
        "permalink": "",
        "status": "starting",
        "error": "",
        "current_step": "",
        "progress_log": []
    }

    async with mcp_tools_session() as tools:
        chain = create_coordinator_chain(tools)
        final_state = await chain.ainvoke(initial_state)

    logger.info(f"🏁 Coordinator Agent pipeline completed - Status: {final_state.get('status')}")

    return {
        "caption": final_state.get("caption", ""),
        "bullets": final_state.get("bullets", []),
        "hashtags": final_state.get("hashtags", ""),
        "image_url": final_state.get("image_url", ""),
        "post_id": final_state.get("post_id", ""),
        "permalink": final_state.get("permalink", ""),
        "status": final_state.get("status", "error"),
        "error": final_state.get("error", ""),
        "current_step": final_state.get("current_step", ""),
        "progress_log": final_state.get("progress_log", [])
    }
