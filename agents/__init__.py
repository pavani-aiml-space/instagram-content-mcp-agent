"""
Multi-Agent System Package

This package contains specialized agents that work together:
- ContentCreatorAgent: Generates Instagram content (captions + hashtags)
- ImageGeneratorAgent: Generates images
- InstagramPosterAgent: Posts content to Instagram
- CoordinatorAgent: Orchestrates all agents as an LCEL RunnableSequence
  (content -> image -> post), with retry on each step
"""

from agents.content_creator_agent import run_content_creator
from agents.image_generator_agent import run_image_generator
from agents.instagram_poster_agent import run_instagram_poster

from agents.coordinator_agent import (
    create_coordinator_chain,
    run_coordinator
)

__all__ = [
    "run_content_creator",
    "run_image_generator",
    "run_instagram_poster",
    "create_coordinator_chain",
    "run_coordinator",
]
