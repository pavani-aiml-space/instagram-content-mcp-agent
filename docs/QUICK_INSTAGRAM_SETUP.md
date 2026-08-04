# Quick Instagram Setup Guide

## Your Current Issue
Your `INSTAGRAM_ACCESS_TOKEN` has expired. You need to:
1. Get a new access token
2. Get your Instagram Account ID
3. Add both to your `.env` file

## Step 1: Get New Access Token (5 minutes)

### Option A: Graph API Explorer (Easiest)

1. Go to: https://developers.facebook.com/tools/explorer/
2. Select your app from the dropdown (or create one if needed)
3. Click **"Generate Access Token"**
4. Select these permissions:
   - ✅ `instagram_basic`
   - ✅ `instagram_content_publish`
   - ✅ `pages_show_list`
   - ✅ `pages_read_engagement`
5. Click **"Generate Access Token"**
6. **Copy the token** - this is your new `INSTAGRAM_ACCESS_TOKEN`

⚠️ **Note**: This token expires in 1-2 hours. For production, you'll need a long-lived token (see Step 3).

## Step 2: Get Instagram Account ID (5 minutes)

### Method 1: Using Graph API Explorer

1. In Graph API Explorer, use your new access token
2. Query: `GET /me/accounts`
3. Find your Facebook Page ID from the response
4. Query: `GET /{your-page-id}?fields=instagram_business_account`
5. Copy the `id` from `instagram_business_account` - this is your `INSTAGRAM_ACCOUNT_ID`

### Method 2: Using the Helper Script

After you get a new access token:

```bash
# Add token to .env first
echo "INSTAGRAM_ACCESS_TOKEN=your_new_token_here" >> .env

# Run the helper script
python scripts/get_instagram_credentials.py
```

Enter your Facebook Page ID when prompted.

### Method 3: Find Facebook Page ID

1. Go to your Facebook Page
2. Click **"About"** (left sidebar)
3. Scroll down to find **"Page ID"**
4. Copy that number

## Step 3: Add to .env File

Add these lines to your `.env` file:

```bash
INSTAGRAM_ACCESS_TOKEN=your_new_token_here
INSTAGRAM_ACCOUNT_ID=your_instagram_account_id_here
```

**Example:**
```bash
INSTAGRAM_ACCESS_TOKEN=EAABwzLixnjYBO7ZC...
INSTAGRAM_ACCOUNT_ID=17841405309211844
```

## Step 4: Verify Setup

```bash
# Test your credentials
python scripts/get_instagram_credentials.py
```

You should see:
```
✅ Access token is valid!
✅ Instagram Business Account ID: 17841405309211844
```

## Step 5: Get Long-Lived Token (For Production)

Short-lived tokens expire in 1-2 hours. For production:

1. Go to: https://developers.facebook.com/tools/debug/accesstoken/
2. Enter your short-lived token
3. Click **"Extend Access Token"**
4. Copy the new long-lived token (expires in 60 days)

Or use this API call:
```bash
curl -X GET "https://graph.facebook.com/v18.0/oauth/access_token?grant_type=fb_exchange_token&client_id={your-app-id}&client_secret={your-app-secret}&fb_exchange_token={your-short-token}"
```

## Quick Reference

### Prerequisites
- ✅ Instagram Business Account (not personal)
- ✅ Facebook Page linked to Instagram
- ✅ Facebook Developer Account

### Quick Links
- **Graph API Explorer**: https://developers.facebook.com/tools/explorer/
- **Token Debugger**: https://developers.facebook.com/tools/debug/accesstoken/
- **Full Guide**: `docs/INSTAGRAM_SETUP_GUIDE.md`

## Troubleshooting

### "Access token expired"
- Get a new token from Graph API Explorer
- For production, use long-lived token

### "No Instagram Business Account linked"
- Make sure your Instagram is a Business account
- Make sure it's linked to your Facebook Page
- Check Facebook Page settings

### "Invalid permissions"
- Make sure you selected all required permissions
- Regenerate token with correct permissions

