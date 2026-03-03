#!/bin/bash
# Start cloudflared tunnel and write URL to file
cloudflared tunnel --url http://localhost:8877 2>&1 | tee /tmp/cf-tunnel.log &
sleep 10
URL=$(grep -o 'https://[a-z\-]*.trycloudflare.com' /tmp/cf-tunnel.log | tail -1)
echo "$URL" > /home/elie/.openclaw/workspace/diner-mathys/tunnel-url.txt
echo "Tunnel URL: $URL"
wait
