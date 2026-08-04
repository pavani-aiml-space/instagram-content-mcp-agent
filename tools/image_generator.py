"""
Image Generator Tool
Generates images using Stability AI or OpenAI Images API
Images are generated without text overlay - caption and bullets are for Instagram post only
"""

import os
import requests
from typing import Dict, Optional, List
from dotenv import load_dotenv
from PIL import Image, ImageDraw, ImageFont
import io
import base64

load_dotenv()


class ImageGenerator:
    """
    Generates images using Stability AI or OpenAI Images API
    
    Supports:
    - Stability AI          -> primary provider (default)
    - OpenAI (gpt-image-1)  -> alternative provider
    """
    
    def __init__(self, provider: Optional[str] = None, api_key: Optional[str] = None):
        """
        Initialize image generator
        
        Args:
            provider: "stability" (default) or "openai"
            api_key: API key (defaults to env vars)
        """
        # ✅ Default to Stability AI; can override with IMAGE_PROVIDER env
        self.provider = (provider or os.getenv("IMAGE_PROVIDER", "stability")).lower()
        
        # OpenAI setup
        if self.provider == "openai":
            self.api_key = api_key or os.getenv("OPENAI_API_KEY")
            if not self.api_key:
                raise ValueError("OpenAI API key is required. Set OPENAI_API_KEY in your environment.")
            
            # Also prep Stability as fallback if available
            self.stability_key = os.getenv("STABILITY_API_KEY")
            if self.stability_key:
                self.api_url = (
                    "https://api.stability.ai/v1/generation/"
                    "stable-diffusion-xl-1024-v1-0/text-to-image"
                )
                self.headers = {
                    "Accept": "application/json",
                    "Authorization": f"Bearer {self.stability_key}",
                }
            else:
                self.api_url = None
                self.headers = None
        
        elif self.provider == "stability":
            # Stability AI setup (default before; now explicit)
            self.api_key = api_key or os.getenv("STABILITY_API_KEY")
            if not self.api_key:
                raise ValueError("Stability AI API key is required. Set STABILITY_API_KEY environment variable.")
            
            self.api_url = (
                "https://api.stability.ai/v1/generation/"
                "stable-diffusion-xl-1024-v1-0/text-to-image"
            )
            self.headers = {
                "Accept": "application/json",
                "Authorization": f"Bearer {self.api_key}",
            }
            self.stability_key = self.api_key
        else:
            raise ValueError(f"Unknown provider: {self.provider}. Use 'openai' or 'stability'.")
    
    def generate(
        self,
        prompt: str,
        aspect_ratio: str = "1:1",
        caption: Optional[str] = None,
        bullets: Optional[List[str]] = None,
        topic_details: Optional[str] = None
    ) -> Dict[str, str]:
        """
        Generate image from text prompt
        
        Args:
            prompt: Text description of the image (high-level concept)
            aspect_ratio: "1:1" (square IG), "16:9", "9:16"
            caption: Optional caption text (not overlaid on image, used for Instagram post caption)
            bullets: Optional list of bullet points (not overlaid on image, used for Instagram post caption)
            topic_details: Optional additional details/context about the topic (used for prompt enhancement)
        
        Returns:
            {
                "image_url": "https://...",
                "image_base64": "...",
                "seed": 12345
            }
        """
        # Aspect ratio mapping (for local resize / overlays)
        aspect_ratios = {
            "1:1": (1024, 1024),
            "4:5": (1024, 1280),  # Instagram feed-friendly portrait
            "16:9": (1344, 768),
            "9:16": (768, 1344),
        }
        
        width, height = aspect_ratios.get(aspect_ratio, (1024, 1024))
        
        import logging
        logger = logging.getLogger(__name__)
        
        # Build prompt from caption, topic, and content
        # Combine prompt with topic_details if provided
        if topic_details and topic_details not in prompt:
            enhanced_prompt = f"{prompt}, {topic_details}"
        else:
            enhanced_prompt = prompt
        
        # Add style guidance to avoid infographics - request photographic/realistic style
        style_guidance = ", professional photography, realistic image, high quality, Instagram-worthy, not an infographic or diagram"
        enhanced_prompt = f"{enhanced_prompt}{style_guidance}"
        
        logger.info("📝 Using prompt for image generation")

        # Route by provider, with a placeholder image as the last-resort fallback
        # so a provider outage doesn't fail the whole content pipeline.
        try:
            if self.provider == "openai":
                try:
                    return self._generate_openai_image(
                        enhanced_prompt, width, height, caption, bullets
                    )
                except Exception as e:
                    logger.warning(
                        f"⚠️ OpenAI image generation failed: {str(e)}. "
                        "Trying Stability AI fallback (if configured)."
                    )
                    if self.stability_key and self.api_url and self.headers:
                        return self._generate_stability_ai(
                            enhanced_prompt, width, height, caption, bullets
                        )
                    else:
                        raise

            elif self.provider == "stability":
                return self._generate_stability_ai(
                    enhanced_prompt, width, height, caption, bullets
                )

            else:
                raise RuntimeError("Invalid provider configuration")
        except Exception as e:
            logger.error(
                f"❌ Image generation failed for all configured providers: {str(e)}. "
                "Using a placeholder image so the pipeline can still complete."
            )
            return self._generate_placeholder_image(prompt, width, height, str(e))
    
    # ------------------------------------------------------------------
    # ✅ NEW: OpenAI images (gpt-image-1)
    # ------------------------------------------------------------------
    def _generate_openai_image(
        self,
        prompt: str,
        width: int,
        height: int,
        caption: Optional[str],
        bullets: Optional[List[str]],
    ) -> Dict[str, str]:
        """
        Generate image using OpenAI Images (gpt-image-1)
        - Uses aspect ratio to pick closest supported size
        - Resizes to (width, height) if needed
        """
        from openai import OpenAI
        from io import BytesIO
        
        api_key = self.api_key or os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not set")
        
        client = OpenAI(api_key=api_key)
        
        # Map width/height to OpenAI-supported sizes
        # gpt-image-1 supports: 1024x1024, 1024x1792 (portrait), 1792x1024 (landscape)
        if width == height:
            size = "1024x1024"
        elif height > width:
            size = "1024x1792"  # portrait-ish
        else:
            size = "1792x1024"  # landscape-ish
        
        # Try gpt-image-1 first (if available), fallback to dall-e-3
        try:
            response = client.images.generate(
                model="gpt-image-1",
                prompt=prompt,
                size=size,
                n=1,
                response_format="b64_json",  # Get base64 directly
            )
            # gpt-image-1 returns base64
            b64 = response.data[0].b64_json
            image_bytes = base64.b64decode(b64)
        except Exception:
            # Fallback to DALL-E 3 (returns URL)
            response = client.images.generate(
                model="dall-e-3",
                prompt=prompt,
                size=size,
                n=1,
            )
            # DALL-E 3 returns URL, so we need to download it
            image_url_from_api = response.data[0].url
            
            # Download the image
            img_response = requests.get(image_url_from_api)
            img_response.raise_for_status()
            image_bytes = img_response.content
        
        # Open with PIL
        img = Image.open(BytesIO(image_bytes))
        
        # Resize to our desired canvas size if different
        if img.size != (width, height):
            img = img.resize((width, height), Image.Resampling.LANCZOS)
            buffer = BytesIO()
            img.save(buffer, format="PNG")
            image_bytes = buffer.getvalue()
            b64 = base64.b64encode(image_bytes).decode("utf-8")
        else:
            b64 = base64.b64encode(image_bytes).decode("utf-8")
        
        # Generate a deterministic-ish seed from prompt
        seed = hash(prompt) % 1000000
        
        # Save image + overlay caption if provided
        image_url = self._save_image(b64, seed, caption=caption, bullets=bullets)
        
        return {
            "image_url": image_url,
            "image_base64": b64,
            "seed": seed,
            "is_placeholder": False,
        }

    # ------------------------------------------------------------------
    # Stability AI (unchanged logic, still used as fallback or primary)
    # ------------------------------------------------------------------
    def _generate_stability_ai(
        self,
        prompt: str,
        width: int,
        height: int,
        caption: Optional[str],
        bullets: Optional[List[str]],
    ) -> Dict[str, str]:
        """Generate image using Stability AI API"""
        if not self.api_url or not self.headers:
            raise RuntimeError("Stability AI is not configured for this instance.")
        
        # Negative prompt to avoid bad images and infographic-style layouts
        negative_prompt = (
            "blurry, low quality, pixelated, distorted, "
            "ugly, bad anatomy, text, watermark, "
            "noise, artifacts, compression, "
            "unprofessional, amateur, cluttered, "
            "infographic, diagram, flowchart, chart, "
            "recipe card, instruction manual, step-by-step guide layout, "
            "text-heavy, boxes with arrows, numbered steps layout"
        )
        
        body = {
            "text_prompts": [
                {
                    "text": prompt,
                    "weight": 1.0,
                },
                {
                    "text": negative_prompt,
                    "weight": -1.0,
                },
            ],
            "cfg_scale": 8,
            "height": height,
            "width": width,
            "samples": 1,
            "steps": 40,
            "style_preset": "photographic",
        }
        
        try:
            response = requests.post(self.api_url, headers=self.headers, json=body)
            
            if response.status_code != 200:
                error_msg = response.json().get("message", "Unknown error")
                raise Exception(f"Stability AI API error: {error_msg}")
            
            data = response.json()
            
            if "artifacts" in data and len(data["artifacts"]) > 0:
                image_base64 = data["artifacts"][0]["base64"]
                seed = data["artifacts"][0].get("seed", 0)
                
                image_url = self._save_image(
                    image_base64, seed, caption=caption, bullets=bullets
                )
                
                return {
                    "image_url": image_url,
                    "image_base64": image_base64,
                    "seed": seed,
                    "is_placeholder": False,
                }
            else:
                raise Exception("No image generated")
        
        except requests.exceptions.RequestException as e:
            raise Exception(f"Error calling Stability AI API: {str(e)}")
        except Exception as e:
            raise Exception(f"Error generating image: {str(e)}")
    
    # ------------------------------------------------------------------
    # Placeholder fallback - used when every configured provider fails
    # ------------------------------------------------------------------
    def _generate_placeholder_image(
        self,
        prompt: str,
        width: int,
        height: int,
        error: str,
    ) -> Dict[str, str]:
        """Build a simple local placeholder image so the pipeline can still
        complete (and post) even when image generation is unavailable."""
        import logging
        logger = logging.getLogger(__name__)

        image = Image.new("RGB", (width, height), color=(60, 63, 74))
        draw = ImageDraw.Draw(image)

        label = "Image unavailable"
        subtitle = prompt[:60] + ("…" if len(prompt) > 60 else "")

        try:
            label_font = ImageFont.load_default(size=42)
            subtitle_font = ImageFont.load_default(size=24)
        except TypeError:
            # Older Pillow without the `size` kwarg on load_default
            label_font = ImageFont.load_default()
            subtitle_font = label_font

        for text, font, y_fraction, fill in (
            (label, label_font, 0.45, (230, 230, 235)),
            (subtitle, subtitle_font, 0.55, (160, 160, 168)),
        ):
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            draw.text(
                ((width - text_width) / 2, height * y_fraction),
                text,
                font=font,
                fill=fill,
            )

        buffer = io.BytesIO()
        image.save(buffer, format="PNG")
        image_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")
        seed = abs(hash(prompt)) % 1000000

        logger.info(f"🖼️ Generated placeholder image (original error: {error})")
        image_url = self._save_image(image_base64, seed)

        return {
            "image_url": image_url,
            "image_base64": image_base64,
            "seed": seed,
            "is_placeholder": True,
        }

    # ------------------------------------------------------------------
    # Everything below here is unchanged from your original (save + overlay)
    # ------------------------------------------------------------------
    def _save_image(
        self,
        image_base64: str,
        seed: int,
        caption: Optional[str] = None,
        bullets: Optional[List[str]] = None,
    ) -> str:
        """
        Save image locally with optional text overlay and return public URL
        """
        import base64
        from datetime import datetime
        import logging
        
        # Decode base64 image
        image_data = base64.b64decode(image_base64)
        
        # Open image with PIL
        image = Image.open(io.BytesIO(image_data))
        
        # Text overlay removed - images are generated without text overlay
        # Caption and bullets are only used in Instagram post caption, not on the image
        
        # Create assets directory if it doesn't exist
        os.makedirs("assets", exist_ok=True)
        
        # Generate filename
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        filename = f"aiimg-{timestamp}-{seed}.png"
        filepath = f"assets/{filename}"
        
        # Save image
        image.save(filepath, "PNG")
        
        public_image_server_url = os.getenv("PUBLIC_IMAGE_SERVER_URL")
        
        logger = logging.getLogger(__name__)
        
        if public_image_server_url:
            base_url = public_image_server_url.rstrip("/")
            image_url = f"{base_url}/assets/{filename}"
            
            logger.info(f"✅ Image saved: {filepath}")
            logger.info(f"🌐 Public URL: {image_url}")
            
            # Verify URL (best-effort)
            try:
                test_response = requests.head(
                    image_url, timeout=5, allow_redirects=True
                )
                if test_response.status_code == 200:
                    logger.info(
                        f"✅ Image URL is accessible (Status: {test_response.status_code})"
                    )
                else:
                    logger.warning(
                        f"⚠️ Image URL returned status {test_response.status_code} - may not be accessible"
                    )
            except Exception as e:
                logger.warning(
                    f"⚠️ Could not verify image URL accessibility: {str(e)}"
                )
            
            return image_url
        else:
            logger.warning(
                "⚠️ PUBLIC_IMAGE_SERVER_URL not set. Image saved locally but Instagram "
                "requires public URL. Set PUBLIC_IMAGE_SERVER_URL in .env "
                "(e.g., from ngrok or localtunnel)"
            )
            return f"file://{os.path.abspath(filepath)}"
    


# Example usage
if __name__ == "__main__":
    generator = ImageGenerator(provider="stability")
    result = generator.generate(
        "Embeddings as points in a vector space showing similar concepts clustered together",
        "1:1",
    )
    print("Image URL:", result["image_url"])
