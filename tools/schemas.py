"""
Shared Pydantic Schemas
Used for LangChain structured LLM output and for MCP tool signatures.
"""

from pydantic import BaseModel, Field


class ContentSchema(BaseModel):
    """
    Structured Instagram content generated from a topic.

    Replaces manual text parsing: the LLM is asked to return exactly
    this shape via ChatOpenAI.with_structured_output(ContentSchema).
    """
    caption: str = Field(
        description="1-3 catchy, engaging opening sentences that hook the reader. "
                    "No markdown, no headings."
    )
    bullets: list[str] = Field(
        description="For a recipe topic: the ingredient list, one ingredient per item. "
                    "For a tech/educational topic: 3-5 key points, one per item, each a short phrase with a brief explanation."
    )
    steps: list[str] = Field(
        description="For a recipe topic: numbered cooking steps, one step per item. "
                    "For a tech/educational topic: a detailed step-by-step explanation, one step per item."
    )
    hashtags: list[str] = Field(
        description="5-10 relevant hashtags, each starting with '#', no duplicates."
    )
