#!/bin/bash
# Start Image Server and Ngrok Tunnel
# This script starts the image server and ngrok tunnel

cd "$(dirname "$0")/.."

echo "=========================================="
echo "Starting Image Server and Ngrok Tunnel"
echo "=========================================="
echo ""

# Check if ngrok is installed
if ! command -v ngrok &> /dev/null; then
    echo "❌ ngrok is not installed"
    echo ""
    echo "Install ngrok:"
    echo "  macOS: brew install ngrok/ngrok/ngrok"
    echo "  Or download from: https://ngrok.com/download"
    echo ""
    exit 1
fi

# Check if image server is already running
if lsof -Pi :8002 -sTCP:LISTEN -t >/dev/null ; then
    echo "⚠️  Image server is already running on port 8002"
    echo "   Kill it first: kill \$(lsof -ti :8002)"
    exit 1
fi

# Check if ngrok is already running
if pgrep -f "ngrok http 8002" > /dev/null; then
    echo "⚠️  ngrok is already running for port 8002"
    echo "   Kill it first: pkill -f 'ngrok http 8002'"
    exit 1
fi

# Start image server in background
echo "1️⃣  Starting image server on port 8002..."
source venv/bin/activate
python scripts/start_image_server.py > /tmp/image_server.log 2>&1 &
IMAGE_SERVER_PID=$!
echo "   Image server started (PID: $IMAGE_SERVER_PID)"
echo "   Logs: tail -f /tmp/image_server.log"
echo ""

# Wait a moment for server to start
sleep 2

# Check if server started
if ! lsof -Pi :8002 -sTCP:LISTEN -t >/dev/null ; then
    echo "❌ Image server failed to start. Check logs: cat /tmp/image_server.log"
    kill $IMAGE_SERVER_PID 2>/dev/null
    exit 1
fi

echo "✅ Image server is running on http://localhost:8002"
echo ""

# Start ngrok
echo "2️⃣  Starting ngrok tunnel..."
echo "   This will give you a public URL"
echo ""

# Start ngrok in background and capture the URL
ngrok http 8002 > /tmp/ngrok.log 2>&1 &
NGROK_PID=$!

# Wait for ngrok to start
sleep 3

# Get the ngrok URL from the API
NGROK_URL=""
for i in {1..10}; do
    sleep 1
    NGROK_URL=$(curl -s http://localhost:4040/api/tunnels 2>/dev/null | grep -o '"public_url":"https://[^"]*"' | head -1 | cut -d'"' -f4)
    if [ ! -z "$NGROK_URL" ]; then
        break
    fi
done

if [ -z "$NGROK_URL" ]; then
    echo "❌ Failed to get ngrok URL"
    echo "   Check ngrok logs: cat /tmp/ngrok.log"
    echo "   Or visit: http://localhost:4040"
    kill $NGROK_PID 2>/dev/null
    kill $IMAGE_SERVER_PID 2>/dev/null
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ Setup complete!"
echo "=========================================="
echo ""
echo "🌐 Ngrok URL: $NGROK_URL"
echo ""
echo "📝 Next steps:"
echo "1. Add to .env: PUBLIC_IMAGE_SERVER_URL=$NGROK_URL"
echo "2. Restart your backend server"
echo ""
echo "📊 Ngrok dashboard: http://localhost:4040"
echo ""
echo "To stop:"
echo "  - Press Ctrl+C or run: ./scripts/stop_image_server.sh"
echo "  - Image server PID: $IMAGE_SERVER_PID"
echo "  - Ngrok PID: $NGROK_PID"
echo ""

