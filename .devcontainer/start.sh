#!/usr/bin/env bash
# Start Turtle Tide when a Codespace boots or you reconnect. A stopped
# Codespace drops the server, so this brings port 8080 back.
set -euo pipefail
root="$(cd "$(dirname "$0")/.." && pwd)"
exec 9>/tmp/turtle-tide-start.lock
flock -n 9 || exit 0

say() {
  printf '%s\n' "$*"
}

if curl -fsS --max-time 2 http://127.0.0.1:8080/ 2>/dev/null | grep -q "Turtle Tide"; then
  say "Turtle Tide is already running on port 8080."
  say "Open the Ports panel and click the globe next to Turtle Tide."
  say "http://127.0.0.1:8080 only works inside this Codespace, not in a browser on your computer."
  exit 0
fi

cd "$root/backend"
setsid python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8080 >> /tmp/turtle-tide.log 2>&1 < /dev/null &
for _ in $(seq 1 40); do
  if curl -fsS --max-time 2 http://127.0.0.1:8080/ 2>/dev/null | grep -q "Turtle Tide"; then
    say "Turtle Tide is running on port 8080."
    say "Open the Ports panel and click the globe next to Turtle Tide."
    say "http://127.0.0.1:8080 only works inside this Codespace, not in a browser on your computer."
    exit 0
  fi
  sleep 1
done
say "Turtle Tide did not start. The log is /tmp/turtle-tide.log"
exit 1
