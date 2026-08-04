# Instagram Setup Guide: Getting Account ID and Access Token

## Overview

To post content to Instagram using the Graph API, you need:
1. **Instagram Business Account ID** - Your Instagram account's unique identifier
2. **Instagram Access Token** - Token that allows your app to post on your behalf

## Prerequisites

Before you start, make sure you have:
- ✅ A **Facebook Page** (required for Instagram Business accounts)
- ✅ An **Instagram Business Account** (not personal account)
- ✅ Your Instagram account linked to the Facebook Page
- ✅ A **Facebook Developer Account** (free)

## Step-by-Step Setup

### Step 1: Convert to Instagram Business Account

1. Open Instagram app on your phone
2. Go to **Settings** → **Account** → **Switch to Professional Account**
3. Choose **Business** (not Creator)
4. Connect to your **Facebook Page** (create one if you don't have it)

### Step 2: Create a Facebook App

1. Go to [Facebook Developers](https://developers.facebook.com/)
2. Click **My Apps** → **Create App**
3. Choose **Business** as the app type
4. Fill in:
   - **App Name**: e.g., "Instagram Content Generator"
   - **App Contact Email**: Your email
5. Click **Create App**

### Step 3: Add Instagram Basic Display Product

1. In your app dashboard, go to **Add Products**
2. Find **Instagram Basic Display** or **Instagram Graph API**
3. Click **Set Up**

### Step 4: Get Access Token

#### Option A: Using Graph API Explorer (Easiest for Testing)

1. Go to [Graph API Explorer](https://developers.facebook.com/tools/explorer/)
2. Select your app from the dropdown
3. Click **Generate Access Token**
4. Select permissions:
   - `instagram_basic`
   - `instagram_content_publish`
   - `pages_show_list`
   - `pages_read_engagement`
5. Click **Generate Access Token**
6. **Copy the token** - this is your `INSTAGRAM_ACCESS_TOKEN`

⚠️ **Note**: This token expires in 1-2 hours. For production, you'll need a long-lived token (see below).

#### Option B: Using Facebook Login (For Production)

1. In your app dashboard, go to **Settings** → **Basic**
2. Add **OAuth Redirect URIs**:
   - `http://localhost:8000/auth/callback` (for testing)
   - Your production URL (for production)
3. Use Facebook Login flow to get user access token
4. Exchange for long-lived token (60 days)

### Step 5: Get Instagram Business Account ID

#### Method 1: Using Graph API Explorer

1. Go to [Graph API Explorer](https://developers.facebook.com/tools/explorer/)
2. Select your app
3. Use your access token
4. Query: `GET /me/accounts`
5. Find your Facebook Page ID
6. Query: `GET /{page-id}?fields=instagram_business_account`
7. Copy the `id` from `instagram_business_account` - this is your `INSTAGRAM_ACCOUNT_ID`

#### Method 2: Using the Setup Script

Run `scripts/get_instagram_credentials.py` (see `docs/QUICK_INSTAGRAM_SETUP.md`), which calls the same Graph API endpoint and prints the Instagram Business Account ID for you.

### Step 6: Get Long-Lived Access Token (For Production)

Short-lived tokens expire in 1-2 hours. For production, get a long-lived token:

1. Go to [Access Token Debugger](https://developers.facebook.com/tools/debug/accesstoken/)
2. Enter your short-lived token
3. Click **Extend Access Token**
4. Copy the new long-lived token (expires in 60 days)

Or use the API:

```bash
curl -X GET "https://graph.facebook.com/v18.0/oauth/access_token?grant_type=fb_exchange_token&client_id={app-id}&client_secret={app-secret}&fb_exchange_token={short-lived-token}"
```

## Environment Variables

Add these to your `.env` file:

```bash
# Instagram Graph API
INSTAGRAM_ACCESS_TOKEN=your_access_token_here
INSTAGRAM_ACCOUNT_ID=your_instagram_account_id_here

# Optional: Facebook Page ID (for getting account ID)
FACEBOOK_PAGE_ID=your_facebook_page_id_here
```

## Testing Your Setup

### Test 1: Verify Access Token

```python
import requests
import os
from dotenv import load_dotenv

load_dotenv()

access_token = os.getenv("INSTAGRAM_ACCESS_TOKEN")
account_id = os.getenv("INSTAGRAM_ACCOUNT_ID")

# Test token
response = requests.get(
    f"https://graph.facebook.com/v18.0/{account_id}",
    params={"access_token": access_token, "fields": "username"}
)

if response.status_code == 200:
    print("✅ Access token is valid!")
    print(f"Username: {response.json()['username']}")
else:
    print("❌ Access token is invalid or expired")
    print(response.json())
```

### Test 2: Test Posting (Dry Run)

```python
from tools.instagram_poster import InstagramPoster

poster = InstagramPoster()

# Test with a dummy image URL (won't actually post)
try:
    result = poster.post_image(
        image_url="https://example.com/test.jpg",
        caption="Test post",
        instagram_account_id=os.getenv("INSTAGRAM_ACCOUNT_ID")
    )
    print("✅ Posting setup is correct!")
except Exception as e:
    print(f"❌ Error: {e}")
```

## Common Issues

### Issue 1: "Invalid Access Token"
- **Solution**: Token may have expired. Generate a new one or use a long-lived token.

### Issue 2: "Instagram Business Account not found"
- **Solution**: 
  - Make sure your Instagram account is a Business account
  - Make sure it's linked to your Facebook Page
  - Check that you're using the correct Facebook Page ID

### Issue 3: "Missing Permissions"
- **Solution**: Make sure your access token has these permissions:
  - `instagram_basic`
  - `instagram_content_publish`
  - `pages_show_list`

### Issue 4: "Page not found"
- **Solution**: 
  - Make sure you have a Facebook Page (not just a profile)
  - Make sure you're an admin of the Page
  - Check the Page ID is correct

## Production Considerations

### 1. Long-Lived Tokens
- Short-lived tokens expire in 1-2 hours
- Long-lived tokens expire in 60 days
- For production, implement token refresh logic

### 2. App Review
- For production, you may need to submit your app for review
- Some permissions require app review by Facebook

### 3. Rate Limits
- Instagram Graph API has rate limits
- Monitor your usage to avoid hitting limits

### 4. Error Handling
- Implement retry logic for failed posts
- Handle token expiration gracefully
- Log errors for debugging

## Resources

- [Instagram Graph API Documentation](https://developers.facebook.com/docs/instagram-api/)
- [Graph API Explorer](https://developers.facebook.com/tools/explorer/)
- [Access Token Debugger](https://developers.facebook.com/tools/debug/accesstoken/)
- [Facebook Developers](https://developers.facebook.com/)

## Quick Reference

```bash
# Get Instagram Account ID from Facebook Page
GET /{page-id}?fields=instagram_business_account&access_token={token}

# Get long-lived token
GET /oauth/access_token?grant_type=fb_exchange_token&client_id={app-id}&client_secret={app-secret}&fb_exchange_token={short-token}

# Test posting (create media container)
POST /{ig-account-id}/media?image_url={url}&caption={caption}&access_token={token}

# Publish media
POST /{ig-account-id}/media_publish?creation_id={id}&access_token={token}
```

