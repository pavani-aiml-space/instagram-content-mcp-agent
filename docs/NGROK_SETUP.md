# Ngrok Setup Guide

## Why Ngrok?

Ngrok is more reliable than localtunnel for Instagram posting because:
- ✅ More stable connections
- ✅ Better performance
- ✅ Instagram can reliably fetch images
- ✅ Free tier available

## Installation

### macOS (using Homebrew)
```bash
brew install ngrok/ngrok/ngrok
```

### Manual Installation
1. Download from: https://ngrok.com/download
2. Extract and add to PATH
3. Sign up for free account: https://dashboard.ngrok.com/signup
4. Get your authtoken from: https://dashboard.ngrok.com/get-started/your-authtoken
5. Configure: `ngrok config add-authtoken <your-token>`

## Quick Start

### Step 1: Start Image Server and Ngrok

```bash
cd /Users/pavanibayappu/mcpprojects/CascadeProjects/instagramapp
./scripts/start_image_server_and_ngrok.sh
```

This will:
- Start the image server on port 8002
- Start ngrok tunnel
- Show you the public URL

### Step 2: Copy the Ngrok URL

You'll see output like:
```
🌐 Ngrok URL: https://abc123.ngrok-free.app
```

### Step 3: Update .env File

Add/update in your `.env`:
```bash
PUBLIC_IMAGE_SERVER_URL=https://abc123.ngrok-free.app
```

### Step 4: Restart Backend Server

Restart your FastAPI server to pick up the new URL.

## Ngrok Dashboard

While ngrok is running, you can view:
- **Web Interface**: http://localhost:4040
- See all requests
- Inspect traffic
- View logs

## Stopping

To stop everything:
```bash
./scripts/stop_image_server.sh
```

Or manually:
```bash
# Stop ngrok
pkill -f "ngrok http 8002"

# Stop image server
kill $(lsof -ti :8002)
```

## Troubleshooting

### Ngrok not installed
```bash
# macOS
brew install ngrok/ngrok/ngrok

# Or download from ngrok.com
```

### Ngrok not authenticated
```bash
# Sign up at https://dashboard.ngrok.com/signup
# Get authtoken from https://dashboard.ngrok.com/get-started/your-authtoken
ngrok config add-authtoken <your-token>
```

### Port already in use
```bash
# Check what's using port 8002
lsof -i :8002

# Kill it
kill $(lsof -ti :8002)
```

### Can't get ngrok URL
- Check ngrok dashboard: http://localhost:4040
- Check logs: `cat /tmp/ngrok.log`
- Make sure ngrok is authenticated

## Free Tier Limits

Ngrok free tier includes:
- ✅ 1 tunnel at a time
- ✅ Random subdomain (changes each restart)
- ✅ HTTPS support
- ✅ Sufficient for development/testing

For production, consider:
- Paid ngrok plan (static domain)
- Or use a proper image hosting service (AWS S3, Cloudinary, etc.)

