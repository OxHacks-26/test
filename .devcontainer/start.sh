#!/usr/bin/env bash
# Start Turtle Tide when a GitHub Codespace boots, then let the forwarded
# port open in the browser. Exit immediately so Codespaces is not blocked.
set -euo pipefail
root="$(cd "$(dirname "$0")/.." && pwd)"
if curl -fsS --max-time 2 http://127.0.0.1:8080/ >/dev/null 2>&1; then
  exit 0
fi
cd "$root/ui"
nohup python3 app.py >> /tmp/turtle-tide.log 2>&1 &
