"""
Content Generator Tool
Generates Instagram caption and hashtags from a topic

Uses LangChain's ChatOpenAI with structured output (a Pydantic schema)
instead of a raw OpenAI call + manual text parsing - the model returns
already-validated, typed fields.
"""

import os
from typing import Dict, Optional
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

from tools.schemas import ContentSchema

load_dotenv()


class ContentGenerator:
    """
    Generates Instagram content (caption + hashtags) from a topic

    Uses OpenAI GPT (via LangChain) to create engaging, Instagram-optimized content
    """

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize content generator

        Args:
            api_key: OpenAI API key (defaults to OPENAI_API_KEY env var)
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API key is required. Set OPENAI_API_KEY environment variable.")

        self.llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0.7,
            max_tokens=1500,
            api_key=self.api_key,
        ).with_structured_output(ContentSchema)

    def _is_recipe_topic(self, topic: str, topic_details: Optional[str] = None) -> bool:
        """Detect if the topic is recipe-related"""
        recipe_keywords = [
            'recipe', 'cooking', 'dish', 'food', 'cuisine', 'ingredient', 'ingredients',
            'bake', 'baking', 'cook', 'meal', 'dish', 'pumpkin pie', 'pie', 'cake',
            'soup', 'curry', 'pasta', 'bread', 'dessert', 'appetizer', 'main course'
        ]
        combined_text = f"{topic} {topic_details or ''}".lower()
        return any(keyword in combined_text for keyword in recipe_keywords)

    def generate(self, topic: str, format: str = "post", topic_details: Optional[str] = None) -> Dict[str, str]:
        """
        Generate Instagram content from topic

        Args:
            topic: Content topic (e.g., "LLM", "AI Agents", "Pumpkin Pie")
            format: Content format - "post", "story", or "reel"
            topic_details: Optional additional details/context about the topic

        Returns:
            {
                "caption": "Full assembled caption text (intro + bullets/steps, recipe headings if applicable)",
                "bullets": ["bullet point 1", "bullet point 2"],
                "hashtags": "#ai #machinelearning #tech"
            }
        """
        is_recipe = self._is_recipe_topic(topic, topic_details)

        topic_description = topic
        if topic_details:
            topic_description = f"{topic}\n\nAdditional context and details:\n{topic_details}"

        if is_recipe:
            prompt = f"""Create an Instagram post caption for a recipe: {topic_description}

- caption: 1-2 catchy, engaging lines that hook the reader (e.g. "Who's ready for the perfect fall dessert? \U0001F342 This pumpkin pie is absolutely divine!")
- bullets: the ingredient list, one ingredient per item
- steps: the numbered cooking steps, one step per item
- hashtags: 5-10 relevant food/recipe hashtags

Use emojis sparingly but effectively. Keep it Instagram-friendly and easy to follow."""
            system_message = "You are an expert food blogger and Instagram content creator. You create engaging, clear recipe posts that are easy to follow and visually appealing."
        else:
            prompt = f"""Create an educational Instagram post about: {topic_description}

- caption: 2-3 engaging sentences explaining the topic and why it matters (context, why this matters, or a relatable example)
- bullets: 3-5 key points, one per item, each a short phrase with a brief explanation
- steps: a detailed step-by-step explanation, one step per item
- hashtags: 5-10 relevant hashtags

Technical but accessible language. Use the provided topic details to create specific, accurate content."""
            system_message = "You are an expert Instagram content creator specializing in AI and technology education. You create educational, technical but accessible content with clear explanations."

        try:
            result: ContentSchema = self.llm.invoke([
                {"role": "system", "content": system_message},
                {"role": "user", "content": prompt},
            ])
        except Exception as e:
            raise Exception(f"Error generating content: {str(e)}")

        caption = self._assemble_caption(result, is_recipe)
        hashtags = result.hashtags or self._generate_default_hashtags(topic).split()

        return {
            "caption": caption,
            "bullets": result.bullets,
            "hashtags": " ".join(hashtags),
        }

    def _assemble_caption(self, content: ContentSchema, is_recipe: bool) -> str:
        """Assemble the final caption text from structured content, matching the
        original recipe/tech formatting (Ingredients:/Recipe: headings for recipes,
        plain bullets/numbered steps for tech posts)."""
        parts = [content.caption.strip()]

        if is_recipe:
            if content.bullets:
                ingredients = "\n".join(f"- {item}" for item in content.bullets)
                parts.append(f"Ingredients:\n{ingredients}")
            if content.steps:
                steps = "\n".join(f"{i}. {step}" for i, step in enumerate(content.steps, start=1))
                parts.append(f"Recipe:\n{steps}")
        else:
            if content.bullets:
                parts.append("\n".join(f"• {item}" for item in content.bullets))
            if content.steps:
                parts.append("\n".join(f"{i}. {step}" for i, step in enumerate(content.steps, start=1)))

        return "\n\n".join(parts).strip()

    def _generate_default_hashtags(self, topic: str) -> str:
        """Generate default hashtags if none found"""
        base_hashtags = ["#ai", "#technology", "#education", "#learning"]
        topic_hashtag = f"#{topic.lower().replace(' ', '')}"
        return f"{topic_hashtag} {' '.join(base_hashtags)}"


# Example usage
if __name__ == "__main__":
    generator = ContentGenerator()
    result = generator.generate("LLM", "post")
    print("Caption:", result["caption"])
    print("\nHashtags:", result["hashtags"])
