"""
Instagram Poster Tool
Posts content and images to Instagram using Graph API
"""

import os
import time
import uuid
import logging
import requests
from typing import Dict, Optional
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)


class InstagramPoster:
    """
    Posts content to Instagram using Instagram Graph API
    
    Handles posting images with captions to Instagram Business accounts
    """
    
    def __init__(self, access_token: Optional[str] = None):
        """
        Initialize Instagram poster
        
        Args:
            access_token: Instagram access token (defaults to INSTAGRAM_ACCESS_TOKEN env var)
        """
        self.access_token = access_token or os.getenv("INSTAGRAM_ACCESS_TOKEN")
        if not self.access_token:
            raise ValueError("Instagram access token is required. Set INSTAGRAM_ACCESS_TOKEN environment variable.")
        
        self.graph_api_base = "https://graph.facebook.com/v18.0"
    
    def post_image(
        self,
        image_url: str,
        caption: str,
        instagram_account_id: str,
        dry_run: bool = False,
        media_type: Optional[str] = None,
    ) -> Dict[str, str]:
        """
        Post image with caption to Instagram

        Args:
            image_url: URL of the image to post (must be publicly accessible HTTP/HTTPS URL)
            caption: Caption text (can include hashtags)
            instagram_account_id: Instagram Business Account ID
            dry_run: If True, validates inputs and logs what would be posted without
                calling the real Graph API.
            media_type: Graph API media_type for the container, e.g. "STORIES". Leave
                None for a plain feed post. "REELS" is intentionally not accepted here:
                the Graph API requires REELS containers to carry a video_url, and this
                poster only ever receives a static image_url, so a caller must not
                pass "REELS" (see post_to_instagram in mcp_server, which rejects it
                before this method is called).

        Returns:
            {
                "post_id": "instagram_post_id",
                "permalink": "https://instagram.com/p/...",
                "status": "success"
            }
        """
        # Validate image URL
        if image_url.startswith("file://"):
            raise Exception(
                f"Image URL must be publicly accessible (HTTP/HTTPS), not a local file. "
                f"Current URL: {image_url}. "
                f"Please set PUBLIC_IMAGE_SERVER_URL in .env and use ngrok/localtunnel to expose your assets folder."
            )
        
        if not (image_url.startswith("http://") or image_url.startswith("https://")):
            raise Exception(
                f"Image URL must be a valid HTTP/HTTPS URL. Got: {image_url}"
            )

        if dry_run:
            fake_post_id = f"DRYRUN-{uuid.uuid4()}"
            logger.info(
                f"[DRY RUN] Would post to Instagram account {instagram_account_id}: "
                f"image_url={image_url}, caption={caption[:100]!r}..."
            )
            return {
                "post_id": fake_post_id,
                "permalink": None,
                "status": "dry_run",
            }

        try:
            # Step 1: Create media container
            container_response = self._create_media_container(
                image_url,
                caption,
                instagram_account_id,
                media_type=media_type,
            )
            
            logger.info(f"📦 Media container response: {container_response}")
            
            # Extract creation_id - Instagram API returns it as "id"
            creation_id = container_response.get("id")
            
            if not creation_id:
                logger.error(f"❌ No 'id' field in container response: {container_response}")
                raise Exception(
                    f"Media container created but no ID returned. Response: {container_response}. "
                    f"This usually means the image URL is not accessible or the media type is invalid."
                )
            
            logger.info(f"✅ Got creation_id: {creation_id}")
            
            # Small delay to ensure media container is ready (Instagram sometimes needs a moment)
            logger.info("⏳ Waiting 2 seconds for media container to be ready...")
            time.sleep(2)
            
            # Step 2: Publish the media container
            publish_response = self._publish_media(creation_id, instagram_account_id)
            
            logger.info(f"✅ Publish response: {publish_response}")
            
            post_id = publish_response.get("id")
            if not post_id:
                logger.error(f"❌ No 'id' field in publish response: {publish_response}")
                raise Exception(
                    f"Media published but no post ID returned. Response: {publish_response}"
                )
            
            return {
                "post_id": post_id,
                "permalink": f"https://www.instagram.com/p/{post_id}/",
                "status": "success",
                "creation_id": creation_id
            }
            
        except Exception as e:
            logger.error(f"❌ Error in post_image: {str(e)}")
            raise Exception(f"Error posting to Instagram: {str(e)}")
    
    def _create_media_container(
        self,
        image_url: str,
        caption: str,
        instagram_account_id: str,
        media_type: Optional[str] = None,
    ) -> Dict:
        """
        Step 1: Create media container (upload image)
        """
        # Log the image URL for debugging
        logger.info(f"📤 Creating media container with image URL: {image_url}")
        
        # Verify the image URL is accessible before sending to Instagram
        try:
            test_response = requests.head(image_url, timeout=10, allow_redirects=True)
            logger.info(f"🔍 Image URL accessibility check: Status {test_response.status_code}")
            
            if test_response.status_code != 200:
                # Try GET to see what we get
                test_get = requests.get(image_url, timeout=10, allow_redirects=True)
                logger.warning(f"⚠️ Image URL returned status {test_get.status_code}, Content-Type: {test_get.headers.get('Content-Type', 'unknown')}")
                
                if test_get.status_code != 200:
                    raise Exception(
                        f"Image URL is not accessible. Status: {test_get.status_code}, "
                        f"URL: {image_url}. Make sure your tunnel is running and PUBLIC_IMAGE_SERVER_URL is correct."
                    )
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Cannot access image URL: {str(e)}")
            raise Exception(
                f"Cannot access image URL: {str(e)}. "
                f"Make sure your image server and tunnel are running. URL: {image_url}"
            )
        
        url = f"{self.graph_api_base}/{instagram_account_id}/media"
        
        params = {
            "image_url": image_url,
            "caption": caption,
            "access_token": self.access_token
        }
        if media_type:
            params["media_type"] = media_type

        logger.info(f"📡 Sending request to Instagram Graph API: {url}")
        logger.info(f"📋 Request params: image_url={image_url[:50]}..., caption length={len(caption)}")
        
        response = requests.post(url, params=params)
        
        logger.info(f"📥 Response status: {response.status_code}")
        
        if response.status_code != 200:
            try:
                error_data = response.json()
                error_msg = error_data.get("error", {}).get("message", "Unknown error")
                error_code = error_data.get("error", {}).get("code", "Unknown")
                error_subcode = error_data.get("error", {}).get("error_subcode", "Unknown")
                logger.error(f"❌ Instagram API error: Code {error_code}, Subcode: {error_subcode}, Message: {error_msg}")
                logger.error(f"❌ Full error response: {error_data}")
                
                # Provide more helpful error messages
                if error_code == 100:
                    raise Exception(
                        f"Invalid parameter: {error_msg}. "
                        f"Check that image_url is publicly accessible and the image format is supported (JPG, PNG)."
                    )
                elif error_code == 2207001:
                    raise Exception(
                        f"Invalid image: {error_msg}. "
                        f"The image URL might not be accessible or the image format is not supported."
                    )
                else:
                    raise Exception(f"Failed to create media container: {error_msg} (Code: {error_code})")
            except ValueError:
                # Response is not JSON
                logger.error(f"❌ Non-JSON error response: {response.text}")
                raise Exception(f"Failed to create media container: HTTP {response.status_code} - {response.text}")
        
        try:
            response_data = response.json()
            logger.info(f"✅ Media container created successfully. Response: {response_data}")
            
            # Verify we have an ID
            if "id" not in response_data:
                logger.warning(f"⚠️ Response missing 'id' field: {response_data}")
                # Sometimes Instagram returns the ID in a different format
                # Check for alternative fields
                if "creation_id" in response_data:
                    response_data["id"] = response_data["creation_id"]
                    logger.info(f"✅ Using 'creation_id' as 'id': {response_data['id']}")
                else:
                    raise Exception(
                        f"Media container response missing 'id' field. Response: {response_data}. "
                        f"This usually means the image URL is not accessible or there's an API issue."
                    )
            
            return response_data
        except ValueError:
            logger.error(f"❌ Invalid JSON response: {response.text}")
            raise Exception(f"Invalid response from Instagram API: {response.text}")
    
    def _publish_media(self, creation_id: str, instagram_account_id: str) -> Dict:
        """
        Step 2: Publish the media container
        """
        if not creation_id:
            raise Exception("Cannot publish media: creation_id is missing or empty")
        
        url = f"{self.graph_api_base}/{instagram_account_id}/media_publish"
        
        params = {
            "creation_id": creation_id,
            "access_token": self.access_token
        }
        
        logger.info(f"📤 Publishing media with creation_id: {creation_id}")
        logger.info(f"📡 Publishing to: {url}")
        
        response = requests.post(url, params=params)
        
        logger.info(f"📥 Publish response status: {response.status_code}")
        
        if response.status_code != 200:
            try:
                error_data = response.json()
                error_msg = error_data.get("error", {}).get("message", "Unknown error")
                error_code = error_data.get("error", {}).get("code", "Unknown")
                error_subcode = error_data.get("error", {}).get("error_subcode", "Unknown")
                logger.error(f"❌ Publish error: Code {error_code}, Subcode: {error_subcode}, Message: {error_msg}")
                logger.error(f"❌ Full error response: {error_data}")
                
                # Provide more helpful error messages
                if "Media ID is not available" in error_msg or error_code == 2207006:
                    raise Exception(
                        f"Media ID is not available. This usually means: "
                        f"1. The media container was not created successfully, "
                        f"2. The creation_id ({creation_id}) is invalid, "
                        f"3. There was a delay and the media container expired, or "
                        f"4. The image URL is not accessible. "
                        f"Original error: {error_msg}"
                    )
                else:
                    raise Exception(f"Failed to publish media: {error_msg} (Code: {error_code})")
            except ValueError:
                logger.error(f"❌ Non-JSON error response: {response.text}")
                raise Exception(f"Failed to publish media: HTTP {response.status_code} - {response.text}")
        
        try:
            response_data = response.json()
            logger.info(f"✅ Media published successfully. Response: {response_data}")
            return response_data
        except ValueError:
            logger.error(f"❌ Invalid JSON response: {response.text}")
            raise Exception(f"Invalid response from Instagram API: {response.text}")


# Example usage
if __name__ == "__main__":
    poster = InstagramPoster()
    # Note: You need to set up Instagram Business Account and get IDs first
    print("Instagram Poster initialized")

