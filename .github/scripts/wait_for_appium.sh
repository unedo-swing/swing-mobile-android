#!/usr/bin/env bash
# Block until the Appium server answers /status, so pytest never races the
# server's startup. Exits non-zero (and dumps the log) if it never comes up.
set -euo pipefail

URL="${APPIUM_SERVER_URL:-http://127.0.0.1:4723}/status"
DEADLINE=$((SECONDS + 90))

until curl -sf "$URL" >/dev/null; do
  if (( SECONDS >= DEADLINE )); then
    echo "::error::Appium did not become ready at $URL within 90s"
    [[ -f appium.log ]] && tail -50 appium.log
    exit 1
  fi
  sleep 2
done

echo "Appium is ready at $URL"
