#!/usr/bin/env python3
"""
Simple HTTP server to serve images from assets/ folder
This makes images publicly accessible for Instagram posting

Usage:
    python scripts/start_image_server.py

Then set in .env:
    PUBLIC_IMAGE_SERVER_URL=http://localhost:8001

Or use ngrok/localtunnel to expose it publicly:
    npx localtunnel --port 8001
    # Then set PUBLIC_IMAGE_SERVER_URL to the tunnel URL
"""

import http.server
import socketserver
import os
from pathlib import Path

# Change to project root directory
project_root = Path(__file__).parent.parent
os.chdir(project_root)

PORT = 8002

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # Add CORS headers to allow access from anywhere
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', '*')
        super().end_headers()
    
    def log_message(self, format, *args):
        # Custom log format
        print(f"[Image Server] {args[0]}")

def main():
    # Ensure assets directory exists
    assets_dir = project_root / "assets"
    assets_dir.mkdir(exist_ok=True)
    
    print("=" * 60)
    print("Image Server for Instagram Posting")
    print("=" * 60)
    print(f"Serving files from: {project_root}")
    print(f"Server running on: http://localhost:{PORT}")
    print(f"Assets directory: {assets_dir}")
    print()
    print("To make it publicly accessible:")
    print("Option 1 (Recommended - ngrok):")
    print("  1. Run: ./scripts/start_image_server_and_ngrok.sh")
    print("  2. Copy the ngrok URL shown")
    print("  3. Add to .env: PUBLIC_IMAGE_SERVER_URL=<ngrok-url>")
    print("  4. Restart your backend server")
    print()
    print("Option 2 (localtunnel):")
    print("  1. In another terminal, run: npx localtunnel --port 8002")
    print("  2. Copy the tunnel URL (e.g., https://abc123.loca.lt)")
    print("  3. Add to .env: PUBLIC_IMAGE_SERVER_URL=https://abc123.loca.lt")
    print("  4. Restart your backend server")
    print()
    print("Press Ctrl+C to stop the server")
    print("=" * 60)
    print()
    
    with socketserver.TCPServer(("", PORT), MyHTTPRequestHandler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n\n✅ Image server stopped")

if __name__ == "__main__":
    main()

