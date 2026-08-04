#!/bin/bash
# Stop Image Server and Tunnel

echo "Stopping image server and tunnel..."

# Kill image server on port 8002
if lsof -ti :8002 > /dev/null 2>&1; then
    echo "Stopping image server on port 8002..."
    kill $(lsof -ti :8002) 2>/dev/null
    sleep 1
    if lsof -ti :8002 > /dev/null 2>&1; then
        kill -9 $(lsof -ti :8002) 2>/dev/null
    fi
    echo "✅ Image server stopped"
else
    echo "ℹ️  No image server running on port 8002"
fi

# Kill ngrok processes
NGROK_PIDS=$(ps aux | grep "ngrok http 8002" | grep -v grep | awk '{print $2}')
if [ ! -z "$NGROK_PIDS" ]; then
    echo "Stopping ngrok processes..."
    echo "$NGROK_PIDS" | xargs kill 2>/dev/null
    sleep 1
    # Force kill if needed
    echo "$NGROK_PIDS" | xargs kill -9 2>/dev/null
    echo "✅ Ngrok stopped"
else
    echo "ℹ️  No ngrok processes found"
fi

# Kill localtunnel processes (legacy)
LT_PIDS=$(ps aux | grep "localtunnel\|lt --port" | grep -v grep | awk '{print $2}')
if [ ! -z "$LT_PIDS" ]; then
    echo "Stopping localtunnel processes..."
    echo "$LT_PIDS" | xargs kill 2>/dev/null
    echo "✅ Localtunnel stopped"
else
    echo "ℹ️  No localtunnel processes found"
fi

echo "Done!"

