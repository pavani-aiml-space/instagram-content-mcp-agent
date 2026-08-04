# Complete Examples: Agents with Multiple Tools Making Real-Life Decisions

## Example 1: Content Creator Agent (Real-Life Decision Making)

### Tools Available to Agent (Free Tools)

```python
# tools/content_tools.py

class LocalLLMTool:
    """MCP Tool: Generates content using local LLM (Ollama/LM Studio) - FREE"""
    name = "local_content_generator"
    
    def execute(self, topic: str, content_type: str = "educational") -> dict:
        # Using Ollama or LM Studio (completely free, runs locally)
        import requests
        
        prompt = self._build_prompt(topic, content_type)
        response = requests.post(
            "http://localhost:11434/api/generate",  # Ollama endpoint
            json={
                "model": "llama2",  # Free open-source model
                "prompt": prompt,
                "stream": False
            }
        )
        
        return {
            "content": response.json()["response"],
            "tool_used": "local_llm",
            "content_type": content_type,
            "cost": 0.00  # Free!
        }
    
    def _build_prompt(self, topic: str, content_type: str) -> str:
        prompts = {
            "educational": f"Create an educational Instagram post about {topic}. Include key concepts, real-world examples, and applications.",
            "entertaining": f"Create an entertaining Instagram post about {topic}. Make it fun, engaging, and shareable.",
            "inspirational": f"Create an inspirational Instagram post about {topic}. Focus on motivation and personal growth.",
            "trending": f"Create a trending Instagram post about {topic}. Make it viral-worthy with hooks and current references."
        }
        return prompts.get(content_type, prompts["educational"])

class HuggingFaceTool:
    """MCP Tool: Generates content using Hugging Face Inference API (Free tier)"""
    name = "huggingface_content_generator"
    
    def execute(self, topic: str, content_type: str = "educational") -> dict:
        # Hugging Face free tier: 1000 requests/month
        import requests
        import os
        
        prompt = f"Create Instagram post about {topic} in {content_type} style"
        response = requests.post(
            "https://api-inference.huggingface.co/models/microsoft/DialoGPT-medium",
            headers={"Authorization": f"Bearer {os.getenv('HF_TOKEN')}"},
            json={"inputs": prompt}
        )
        
        return {
            "content": response.json()[0]["generated_text"],
            "tool_used": "huggingface",
            "content_type": content_type,
            "cost": 0.00  # Free tier
        }

class OpenAIGPTTool:
    """MCP Tool: Generates content using OpenAI GPT (Paid, but best quality)"""
    name = "openai_gpt_generator"
    
    def execute(self, topic: str, content_type: str = "educational") -> dict:
        # OpenAI GPT-4 (paid, but highest quality)
        import openai
        import os
        
        openai.api_key = os.getenv("OPENAI_API_KEY")
        
        prompt = self._build_prompt(topic, content_type)
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{
                "role": "user",
                "content": prompt
            }],
            temperature=0.7
        )
        
        return {
            "content": response.choices[0].message.content,
            "tool_used": "openai_gpt",
            "content_type": content_type,
            "cost": 0.03  # ~$0.03 per request (GPT-4)
        }
    
    def _build_prompt(self, topic: str, content_type: str) -> str:
        prompts = {
            "educational": f"Create an educational Instagram post about {topic}. Include key concepts, real-world examples, and applications. Make it engaging and easy to understand.",
            "entertaining": f"Create an entertaining Instagram post about {topic}. Make it fun, engaging, and shareable. Use humor and relatable examples.",
            "inspirational": f"Create an inspirational Instagram post about {topic}. Focus on motivation, personal growth, and actionable insights.",
            "trending": f"Create a trending Instagram post about {topic}. Make it viral-worthy with hooks, current references, and shareable content."
        }
        return prompts.get(content_type, prompts["educational"])

class GeminiFlashTool:
    """MCP Tool: Generates content using Google Gemini Flash (Free tier available, fast)"""
    name = "gemini_flash_generator"
    
    def execute(self, topic: str, content_type: str = "educational") -> dict:
        # Google Gemini Flash (free tier: 15 requests/minute, fast and efficient)
        import google.generativeai as genai
        import os
        
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        prompt = self._build_prompt(topic, content_type)
        response = model.generate_content(prompt)
        
        return {
            "content": response.text,
            "tool_used": "gemini_flash",
            "content_type": content_type,
            "cost": 0.00  # Free tier available (15 req/min)
        }
    
    def _build_prompt(self, topic: str, content_type: str) -> str:
        prompts = {
            "educational": f"Create an educational Instagram post about {topic}. Include key concepts, real-world examples, and applications. Make it engaging and easy to understand.",
            "entertaining": f"Create an entertaining Instagram post about {topic}. Make it fun, engaging, and shareable. Use humor and relatable examples.",
            "inspirational": f"Create an inspirational Instagram post about {topic}. Focus on motivation, personal growth, and actionable insights.",
            "trending": f"Create a trending Instagram post about {topic}. Make it viral-worthy with hooks, current references, and shareable content."
        }
        return prompts.get(content_type, prompts["educational"])

class GeminiProTool:
    """MCP Tool: Generates content using Google Gemini Pro (Paid, high quality)"""
    name = "gemini_pro_generator"
    
    def execute(self, topic: str, content_type: str = "educational") -> dict:
        # Google Gemini Pro (paid, but high quality and cost-effective)
        import google.generativeai as genai
        import os
        
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        model = genai.GenerativeModel('gemini-1.5-pro')
        
        prompt = self._build_prompt(topic, content_type)
        response = model.generate_content(prompt)
        
        return {
            "content": response.text,
            "tool_used": "gemini_pro",
            "content_type": content_type,
            "cost": 0.001  # ~$0.001 per request (very cost-effective)
        }
    
    def _build_prompt(self, topic: str, content_type: str) -> str:
        prompts = {
            "educational": f"Create an educational Instagram post about {topic}. Include key concepts, real-world examples, and applications. Make it engaging and easy to understand.",
            "entertaining": f"Create an entertaining Instagram post about {topic}. Make it fun, engaging, and shareable. Use humor and relatable examples.",
            "inspirational": f"Create an inspirational Instagram post about {topic}. Focus on motivation, personal growth, and actionable insights.",
            "trending": f"Create a trending Instagram post about {topic}. Make it viral-worthy with hooks, current references, and shareable content."
        }
        return prompts.get(content_type, prompts["educational"])

class TrendingTopicsTool:
    """MCP Tool: Checks if topic is trending (Free APIs)"""
    name = "trending_topics_checker"
    
    def execute(self, topic: str) -> dict:
        # Using free APIs like Google Trends, Twitter Trends, etc.
        import requests
        
        # Check Google Trends (free)
        trends_response = requests.get(
            f"https://trends.google.com/trends/api/explore?q={topic}"
        )
        
        # Check if topic is trending
        is_trending = self._analyze_trends(trends_response.json(), topic)
        
        return {
            "is_trending": is_trending,
            "trend_score": 0.85 if is_trending else 0.3,
            "recommendation": "capitalize_now" if is_trending else "normal_post"
        }
    
    def _analyze_trends(self, trends_data: dict, topic: str) -> bool:
        # Analyze trend data (simplified)
        return trends_data.get("interest_over_time", {}).get("value", 0) > 50

class EngagementAnalyzerTool:
    """MCP Tool: Analyzes what content type performs best (Free analytics)"""
    name = "engagement_analyzer"
    
    def execute(self, user_id: str) -> dict:
        # Analyze past posts to see what works (using Instagram Basic Display API - free)
        # Returns which content type gets most engagement
        
        return {
            "best_content_type": "educational",  # Based on past performance
            "best_posting_time": "18:00",  # When audience is most active
            "best_format": "carousel",  # Single image vs carousel vs reel
            "avg_engagement_rate": 0.045  # 4.5% engagement rate
        }

class FormatDecisionTool:
    """MCP Tool: Decides between Post, Story, or Reel based on performance and context"""
    name = "format_decision_tool"
    
    def execute(self, user_id: str, topic: str, trending_data: dict, content_type: str) -> dict:
        """
        Real-life decision: Should this be a Post, Story, or Reel?
        Decision factors:
        - What format performs best for this user?
        - Is topic trending? → Reel might be better for viral content
        - Content type? → Educational might work better as carousel post
        - Time of day? → Stories are better for quick updates
        """
        # Analyze past performance by format
        format_performance = self._analyze_format_performance(user_id)
        
        # Decision logic
        recommended_format = self._decide_format(
            format_performance, 
            trending_data, 
            content_type
        )
        
        return {
            "recommended_format": recommended_format,  # "post", "story", or "reel"
            "reason": self._get_reason(recommended_format, trending_data, content_type),
            "format_performance": format_performance,
            "engagement_prediction": self._predict_engagement(recommended_format, format_performance)
        }
    
    def _analyze_format_performance(self, user_id: str) -> dict:
        """
        Analyze which format (post/story/reel) performs best for this user
        Using Instagram Basic Display API to get analytics
        """
        # Simulated analysis based on past posts
        # In real implementation, would query Instagram API
        return {
            "post": {
                "avg_engagement": 0.045,  # 4.5%
                "avg_reaches": 5000,
                "best_time": "18:00",
                "best_content_type": "educational"
            },
            "story": {
                "avg_engagement": 0.08,  # 8% (stories have higher engagement)
                "avg_reaches": 3000,
                "best_time": "12:00",  # Midday for stories
                "best_content_type": "entertaining"
            },
            "reel": {
                "avg_engagement": 0.12,  # 12% (reels have highest engagement)
                "avg_reaches": 10000,
                "best_time": "19:00",
                "best_content_type": "trending"
            }
        }
    
    def _decide_format(self, format_performance: dict, trending_data: dict, content_type: str) -> str:
        """
        Decision logic for format selection
        """
        # If topic is highly trending, recommend Reel (best for viral content)
        if trending_data["is_trending"] and trending_data["trend_score"] > 0.8:
            return "reel"
        
        # If content is trending style, recommend Reel
        if content_type == "trending":
            return "reel"
        
        # If content is entertaining, Stories work well
        if content_type == "entertaining":
            # Check if story performance is good
            if format_performance["story"]["avg_engagement"] > 0.07:
                return "story"
        
        # If content is educational, Posts (carousel) work best
        if content_type == "educational":
            return "post"
        
        # Default: Use format with highest engagement
        best_format = max(
            format_performance.items(),
            key=lambda x: x[1]["avg_engagement"]
        )[0]
        
        return best_format
    
    def _get_reason(self, format: str, trending_data: dict, content_type: str) -> str:
        """Get reason for format recommendation"""
        reasons = {
            "reel": f"Reel recommended because topic is {'trending' if trending_data['is_trending'] else 'suitable for video'} and reels have highest engagement",
            "story": f"Story recommended for {content_type} content - quick, engaging format",
            "post": f"Post recommended for {content_type} content - allows detailed information and carousel format"
        }
        return reasons.get(format, "Post recommended as default format")
    
    def _predict_engagement(self, format: str, format_performance: dict) -> float:
        """Predict engagement rate for recommended format"""
        return format_performance[format]["avg_engagement"]

class HashtagGeneratorTool:
    """MCP Tool: Generates relevant hashtags (Free)"""
    name = "hashtag_generator"
    
    def execute(self, topic: str, content_type: str) -> list:
        # Generate hashtags based on topic and content type
        base_hashtags = [f"#{topic.replace(' ', '')}", "#AIEducation", "#TechTips"]
        
        if content_type == "educational":
            base_hashtags.extend(["#LearnAI", "#TechEducation", "#AILearning"])
        elif content_type == "trending":
            base_hashtags.extend(["#Trending", "#Viral", "#AITrends"])
        
        return base_hashtags
```

### Agent with Real-Life Decision-Making Logic

```python
# agents/content_creator.py

from tools.content_tools import (
    LocalLLMTool,
    HuggingFaceTool,
    OpenAIGPTTool,
    GeminiFlashTool,
    GeminiProTool,
    TrendingTopicsTool,
    EngagementAnalyzerTool,
    HashtagGeneratorTool,
    FormatDecisionTool
)

class ContentCreatorAgent:
    """
    Content Creator Agent with real-life decision-making
    Makes decisions based on: trending topics, audience engagement, content type
    Has access to: 
    - Free: Local LLM, Hugging Face, Gemini Flash (free tier)
    - Paid: OpenAI GPT, Gemini Pro
    """
    def __init__(self, user_id: str):
        # Agent has access to MULTIPLE tools (free + paid options)
        self.local_llm = LocalLLMTool()      # Free, always available
        self.huggingface = HuggingFaceTool() # Free tier
        self.gemini_flash = GeminiFlashTool() # Free tier (15 req/min)
        self.gemini_pro = GeminiProTool()    # Paid, cost-effective
        self.openai_gpt = OpenAIGPTTool()    # Paid, best quality
        self.trending_checker = TrendingTopicsTool()
        self.engagement_analyzer = EngagementAnalyzerTool()
        self.hashtag_generator = HashtagGeneratorTool()
        self.format_decision = FormatDecisionTool()
        
        self.user_id = user_id
        self.decision_history = []
    
    def generate(self, topic: str, context: dict = None) -> dict:
        """
        Agent makes REAL-LIFE decisions:
        - Is topic trending? → Use trending content style
        - What content type performs best? → Use that format
        - What time to post? → Optimize for engagement
        - Which hashtags? → Generate relevant ones
        """
        print(f"\n🤖 Content Creator Agent: Generating content for '{topic}'")
        
        # DECISION 1: Check if topic is trending
        trending_data = self.trending_checker.execute(topic)
        print(f"📈 Trending check: {trending_data['is_trending']} (score: {trending_data['trend_score']})")
        
        # DECISION 2: Analyze what content type performs best for this user
        engagement_data = self.engagement_analyzer.execute(self.user_id)
        print(f"📊 Best performing content type: {engagement_data['best_content_type']}")
        print(f"⏰ Best posting time: {engagement_data['best_posting_time']}")
        
        # DECISION 3: Choose content type based on trending + engagement
        content_type = self._decide_content_type(trending_data, engagement_data, context)
        print(f"✅ Decision: Using '{content_type}' content type")
        
        # DECISION 4: Choose generation tool based on context
        # Decision factors: trending status, quality needs, budget
        llm_tool = self._decide_llm_tool(trending_data, context)
        print(f"🔄 Decision: Using {llm_tool.name} for content generation")
        
        try:
            content = llm_tool.execute(topic, content_type)
        except Exception as e:
            # Fallback strategy: try next best option
            print(f"⚠️  {llm_tool.name} failed, trying fallback...")
            content = self._fallback_llm_tool(llm_tool, topic, content_type)
        
        # DECISION 5: Decide format (Post, Story, or Reel)
        format_decision = self.format_decision.execute(
            self.user_id, 
            topic, 
            trending_data, 
            content_type
        )
        print(f"📱 Decision: Recommended format is '{format_decision['recommended_format']}'")
        print(f"💡 Reason: {format_decision['reason']}")
        print(f"📊 Predicted engagement: {format_decision['engagement_prediction']*100:.1f}%")
        
        # DECISION 6: Generate hashtags based on topic and content type
        hashtags = self.hashtag_generator.execute(topic, content_type)
        print(f"🏷️  Generated {len(hashtags)} hashtags")
        
        # DECISION 7: Optimize posting time based on format
        optimal_time = self._get_optimal_time(format_decision["recommended_format"], engagement_data)
        print(f"⏰ Optimal posting time: {optimal_time}")
        
        # Record decision
        self.decision_history.append({
            "topic": topic,
            "content_type": content_type,
            "format": format_decision["recommended_format"],
            "is_trending": trending_data["is_trending"],
            "tool_used": content["tool_used"],
            "optimal_posting_time": optimal_time
        })
        
        return {
            "content": content["content"],
            "content_type": content_type,
            "format": format_decision["recommended_format"],  # "post", "story", or "reel"
            "format_reason": format_decision["reason"],
            "predicted_engagement": format_decision["engagement_prediction"],
            "hashtags": hashtags,
            "is_trending": trending_data["is_trending"],
            "optimal_posting_time": optimal_time,
            "tool_used": content["tool_used"]
        }
    
    def _get_optimal_time(self, format: str, engagement_data: dict) -> str:
        """Get optimal posting time based on format"""
        format_times = {
            "post": engagement_data.get("best_posting_time", "18:00"),
            "story": "12:00",  # Stories perform best midday
            "reel": "19:00"    # Reels perform best in evening
        }
        return format_times.get(format, engagement_data.get("best_posting_time", "18:00"))
    
    def _decide_content_type(self, trending_data: dict, engagement_data: dict, context: dict) -> str:
        """
        Real-life decision: What content type should we use?
        """
        # If topic is trending, capitalize on it
        if trending_data["is_trending"] and trending_data["trend_score"] > 0.7:
            print("🔥 Decision: Topic is trending! Using trending content style")
            return "trending"
        
        # If user explicitly wants a type, use it
        if context and context.get("content_type"):
            return context["content_type"]
        
        # Otherwise, use what performs best for this user
        return engagement_data["best_content_type"]
    
    def _decide_llm_tool(self, trending_data: dict, context: dict):
        """
        Real-life decision: Which LLM tool should we use?
        Decision factors:
        - Is topic trending? → Use OpenAI/Gemini Pro (best quality for viral content)
        - Quality requirement? → Use OpenAI/Gemini Pro if premium
        - Speed requirement? → Use Gemini Flash (fast, free tier)
        - Budget constraint? → Use free options (Local, Hugging Face, Gemini Flash)
        - Default → Try local (free), then Gemini Flash, then Hugging Face, then paid options
        """
        # If topic is highly trending, use best quality (OpenAI or Gemini Pro)
        if trending_data["is_trending"] and trending_data["trend_score"] > 0.8:
            print("🔥 Decision: High trending score, using best quality tool")
            # Prefer Gemini Pro (cost-effective) or OpenAI (best quality)
            if context and context.get("prefer_gemini"):
                return self.gemini_pro
            return self.openai_gpt
        
        # If user wants premium quality
        if context and context.get("quality") == "premium":
            print("⭐ Decision: Premium quality requested")
            if context.get("prefer_gemini"):
                return self.gemini_pro
            return self.openai_gpt
        
        # If user needs fast generation, use Gemini Flash (free tier, fast)
        if context and context.get("speed") == "fast":
            print("⚡ Decision: Fast generation needed, using Gemini Flash (free, fast)")
            return self.gemini_flash
        
        # If user has budget constraint, prefer free options
        if context and context.get("budget") == "low":
            print("💰 Decision: Low budget, trying free options first")
            # Priority: Local LLM → Gemini Flash → Hugging Face
            try:
                import requests
                requests.get("http://localhost:11434/api/tags", timeout=1)
                return self.local_llm
            except:
                # Try Gemini Flash (free tier, fast)
                try:
                    return self.gemini_flash
                except:
                    return self.huggingface
        
        # Default strategy: Try free options first, then paid
        # Priority: Local LLM → Gemini Flash → Hugging Face → Gemini Pro → OpenAI
        try:
            # Check if local LLM is available
            import requests
            requests.get("http://localhost:11434/api/tags", timeout=1)
            print("✅ Local LLM available, using it (free)")
            return self.local_llm
        except:
            # Try Gemini Flash (free tier, fast, reliable)
            try:
                print("✅ Using Gemini Flash (free tier, fast)")
                return self.gemini_flash
            except:
                # Try Hugging Face (free tier)
                print("⚠️  Using Hugging Face (free tier)")
                return self.huggingface
    
    def _fallback_llm_tool(self, failed_tool, topic: str, content_type: str):
        """
        Fallback strategy if primary tool fails
        Priority: Free options first, then paid
        """
        # If OpenAI failed, try free options first
        if failed_tool == self.openai_gpt:
            try:
                return self.gemini_flash.execute(topic, content_type)
            except:
                try:
                    return self.local_llm.execute(topic, content_type)
                except:
                    return self.huggingface.execute(topic, content_type)
        
        # If Gemini Pro failed, try other options
        elif failed_tool == self.gemini_pro:
            try:
                return self.gemini_flash.execute(topic, content_type)
            except:
                try:
                    return self.openai_gpt.execute(topic, content_type)
                except:
                    return self.local_llm.execute(topic, content_type)
        
        # If local LLM failed, try other free options
        elif failed_tool == self.local_llm:
            try:
                return self.gemini_flash.execute(topic, content_type)
            except:
                try:
                    return self.huggingface.execute(topic, content_type)
                except:
                    # Last resort: Paid options
                    try:
                        return self.gemini_pro.execute(topic, content_type)
                    except:
                        return self.openai_gpt.execute(topic, content_type)
        
        # If Gemini Flash failed, try other options
        elif failed_tool == self.gemini_flash:
            try:
                return self.local_llm.execute(topic, content_type)
            except:
                try:
                    return self.huggingface.execute(topic, content_type)
                except:
                    try:
                        return self.gemini_pro.execute(topic, content_type)
                    except:
                        return self.openai_gpt.execute(topic, content_type)
        
        # If Hugging Face failed, try other options
        else:
            try:
                return self.gemini_flash.execute(topic, content_type)
            except:
                try:
                    return self.gemini_pro.execute(topic, content_type)
                except:
                    return self.openai_gpt.execute(topic, content_type)
```

---

## Example 2: Image Generator Agent (Real-Life Decision Making)

### Tools Available to Agent (Free Tools)

```python
# tools/image_tools.py

class StableDiffusionLocalTool:
    """MCP Tool: Generates images using Stable Diffusion (Local, Free)"""
    name = "stable_diffusion_local"
    
    def execute(self, prompt: str, style: str = "realistic") -> dict:
        # Using Stable Diffusion running locally (completely free)
        import requests
        
        style_prompts = {
            "realistic": f"photorealistic, high quality, {prompt}",
            "artistic": f"artistic, creative, vibrant colors, {prompt}",
            "minimalist": f"minimalist, clean, simple, {prompt}",
            "trending": f"trending style, modern, eye-catching, {prompt}"
        }
        
        response = requests.post(
            "http://localhost:7860/api/v1/txt2img",  # Local Stable Diffusion
            json={
                "prompt": style_prompts.get(style, prompt),
                "steps": 20,
                "width": 1024,
                "height": 1024
            }
        )
        
        return {
            "image_url": response.json()["images"][0],
            "tool_used": "stable_diffusion_local",
            "style": style,
            "cost": 0.00  # Free!
        }

class HuggingFaceImageTool:
    """MCP Tool: Generates images using Hugging Face (Free tier)"""
    name = "huggingface_image_generator"
    
    def execute(self, prompt: str, style: str = "realistic") -> dict:
        # Hugging Face free tier for image generation
        import requests
        
        response = requests.post(
            "https://api-inference.huggingface.co/models/runwayml/stable-diffusion-v1-5",
            headers={"Authorization": f"Bearer {os.getenv('HF_TOKEN')}"},
            json={"inputs": prompt}
        )
        
        return {
            "image_url": self._save_image(response.content),
            "tool_used": "huggingface",
            "style": style,
            "cost": 0.00  # Free tier
        }

class ImageStyleAnalyzerTool:
    """MCP Tool: Analyzes what image style performs best (Free analytics)"""
    name = "image_style_analyzer"
    
    def execute(self, user_id: str) -> dict:
        # Analyze which image styles get most engagement
        return {
            "best_style": "realistic",  # Based on past performance
            "best_aspect_ratio": "1:1",  # Square for Instagram
            "color_preference": "vibrant",  # What colors perform best
            "avg_engagement": 0.052  # 5.2% engagement for images
        }

class ImageOptimizerTool:
    """MCP Tool: Optimizes images for Instagram (Free, local)"""
    name = "image_optimizer"
    
    def execute(self, image_url: str, format: str = "carousel") -> dict:
        # Using PIL/Pillow (free) to optimize images
        from PIL import Image
        import requests
        
        # Download and optimize
        img = Image.open(requests.get(image_url, stream=True).raw)
        
        # Resize for Instagram format
        if format == "carousel":
            img = img.resize((1080, 1080))  # Square
        elif format == "story":
            img = img.resize((1080, 1920))  # Vertical
        
        # Save optimized version
        optimized_path = image_url.replace(".jpg", "_optimized.jpg")
        img.save(optimized_path, quality=85, optimize=True)
        
        return {
            "optimized_url": optimized_path,
            "format": format,
            "size_kb": os.path.getsize(optimized_path) / 1024
        }
```

### Agent with Real-Life Decision-Making Logic

```python
# agents/image_generator.py

from tools.image_tools import (
    StableDiffusionLocalTool,
    HuggingFaceImageTool,
    ImageStyleAnalyzerTool,
    ImageOptimizerTool
)

class ImageGeneratorAgent:
    """
    Image Generator Agent with real-life decision-making
    Makes decisions based on: audience preferences, content format, trending styles
    """
    def __init__(self, user_id: str):
        # Agent has access to MULTIPLE free tools
        self.stable_diffusion = StableDiffusionLocalTool()
        self.huggingface = HuggingFaceImageTool()
        self.style_analyzer = ImageStyleAnalyzerTool()
        self.optimizer = ImageOptimizerTool()
        
        self.user_id = user_id
        self.decision_history = []
    
    def generate(self, prompt: str, content_type: str, recommended_format: str) -> dict:
        """
        Agent makes REAL-LIFE decisions:
        - What image style performs best? → Use that style
        - What format (carousel/story)? → Optimize for format
        - Which free tool is available? → Use what's working
        """
        print(f"\n🎨 Image Generator Agent: Generating image for '{prompt[:50]}...'")
        
        # DECISION 1: Analyze what image style performs best
        style_data = self.style_analyzer.execute(self.user_id)
        print(f"📊 Best performing style: {style_data['best_style']}")
        print(f"📐 Best aspect ratio: {style_data['best_aspect_ratio']}")
        
        # DECISION 2: Choose style based on content type and performance
        image_style = self._decide_image_style(content_type, style_data)
        print(f"✅ Decision: Using '{image_style}' image style")
        
        # DECISION 3: Choose generation tool (prefer local, fallback to Hugging Face)
        try:
            print("🔄 Decision: Trying Stable Diffusion local (free, fast)")
            image = self.stable_diffusion.execute(prompt, image_style)
        except Exception as e:
            print(f"⚠️  Local unavailable, using Hugging Face (free tier)")
            image = self.huggingface.execute(prompt, image_style)
        
        # DECISION 4: Optimize image for recommended format
        print(f"📐 Decision: Optimizing for {recommended_format} format")
        optimized = self.optimizer.execute(image["image_url"], recommended_format)
        print(f"✅ Optimized: {optimized['size_kb']:.1f}KB")
        
        # Record decision
        self.decision_history.append({
            "prompt": prompt[:50],
            "style": image_style,
            "format": recommended_format,
            "tool_used": image["tool_used"]
        })
        
        return {
            "image_url": optimized["optimized_url"],
            "style": image_style,
            "format": recommended_format,
            "tool_used": image["tool_used"]
        }
    
    def _decide_image_style(self, content_type: str, style_data: dict) -> str:
        """
        Real-life decision: What image style should we use?
        """
        # If content is trending, use trending style
        if content_type == "trending":
            return "trending"
        
        # If content is artistic, use artistic style
        if content_type == "entertaining":
            return "artistic"
        
        # Otherwise, use what performs best for this user
        return style_data["best_style"]
```

---

## Complete Flow: Real-Life Decision Making

```python
# Example: Coordinator using both agents with real-life decisions

from agents.content_creator import ContentCreatorAgent
from agents.image_generator import ImageGeneratorAgent

class CoordinatorAgent:
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.content_agent = ContentCreatorAgent(user_id)
        self.image_agent = ImageGeneratorAgent(user_id)
    
    def generate_post(self, topic: str) -> dict:
        """
        Real-life workflow with intelligent decisions
        """
        print(f"\n🎯 Coordinator: Generating post for '{topic}'")
        
        # Content agent makes decisions:
        # - Is topic trending?
        # - What content type performs best?
        # - What time to post?
        content = self.content_agent.generate(topic)
        
        # Image agent makes decisions:
        # - What image style performs best?
        # - What format to use?
        image = self.image_agent.generate(
            prompt=content["content"][:100],  # Use part of content as image prompt
            content_type=content["content_type"],
            recommended_format=content["recommended_format"]
        )
        
        return {
            "content": content["content"],
            "image_url": image["image_url"],
            "hashtags": content["hashtags"],
            "format": content["format"],  # "post", "story", or "reel"
            "format_reason": content["format_reason"],
            "predicted_engagement": content["predicted_engagement"],
            "optimal_posting_time": content["optimal_posting_time"],
            "is_trending": content["is_trending"],
            "recommendations": {
                "post_now": content["is_trending"],  # Post immediately if trending
                "format": content["format"],
                "needs_video": content["format"] == "reel",  # Reels need video
                "needs_multiple_images": content["format"] == "post"  # Posts can be carousel
            }
        }

# Usage
coordinator = CoordinatorAgent(user_id="influencer_123")
result = coordinator.generate_post("Neural Networks")

print(f"\n📝 Content: {result['content'][:100]}...")
print(f"🖼️  Image: {result['image_url']}")
print(f"🏷️  Hashtags: {', '.join(result['hashtags'][:5])}")
print(f"⏰ Post at: {result['optimal_posting_time']}")
print(f"🔥 Trending: {result['is_trending']}")
```

---

## Key Real-Life Decisions Made

### Content Creator Agent:
1. ✅ **Is topic trending?** → Use trending content style
2. ✅ **What content type performs best?** → Use that format
3. ✅ **Post, Story, or Reel?** → Decide based on performance and context
4. ✅ **What time to post?** → Optimize for engagement and format
5. ✅ **Which hashtags?** → Generate relevant ones
6. ✅ **Which LLM tool?** → Prefer free options, use paid for trending/premium

### Image Generator Agent:
1. ✅ **What image style performs best?** → Use that style
2. ✅ **What format?** → Optimize for carousel/story
3. ✅ **Which tool?** → Prefer local Stable Diffusion, fallback to Hugging Face
4. ✅ **Optimize image?** → Resize and compress for Instagram

---

## Tools Available (Free + Paid Options)

### Free Tools:
- ✅ **Local LLM** (Ollama/LM Studio) - Completely free, runs locally
- ✅ **Gemini Flash** - Free tier (15 requests/minute), fast and efficient
- ✅ **Hugging Face** - Free tier (1000 requests/month)
- ✅ **Stable Diffusion Local** - Completely free, runs locally
- ✅ **Instagram Basic Display API** - Free for analytics
- ✅ **Google Trends API** - Free
- ✅ **PIL/Pillow** - Free image processing

### Paid Options (Best Quality):
- 💰 **Gemini Pro** - Paid (~$0.001/request), cost-effective, high quality
  - Used when: Good quality needed, cost-effective option
- 💰 **OpenAI GPT-4** - Paid (~$0.03/request), highest quality
  - Used when: Topic is highly trending, premium quality needed

### Decision Strategy:
1. **Default**: Try free tools first (Local LLM → Gemini Flash → Hugging Face)
2. **Fast generation**: Use Gemini Flash (free tier, fast)
3. **High trending**: Use OpenAI GPT or Gemini Pro for best quality
4. **Premium quality**: Use OpenAI GPT or Gemini Pro if requested
5. **Budget constraint**: Stick to free options only (Local, Gemini Flash, Hugging Face)
6. **Cost-effective quality**: Use Gemini Pro (cheaper than OpenAI, good quality)
7. **Fallback**: If one tool fails, try next in priority order
