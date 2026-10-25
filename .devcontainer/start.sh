#!/usr/bin/env bash
# Start the full Turtle Tide UI when a GitHub Codespace boots. The map is one
# panel inside that page, served at /map/, not the site itself.
set -euo pipefail
root="$(cd "$(dirname "$0")/.." && pwd)"
if curl -fsS --max-time 2 http://127.0.0.1:8080/ | grep -q "Turtle Tide"; then
  exit 0
fi
cd "$root/backend"
setsid python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8080 >> /tmp/turtle-tide.log 2>&1 < /dev/null &
for _ in $(seq 1 40); do
  if curl -fsS --max-time 2 http://127.0.0.1:8080/ | grep -q "Turtle Tide"; then
    exit 0
  fi
  sleep 1
done
echo "Turtle Tide did not serve the full UI. See /tmp/turtle-tide.log" >&2
exit 1
