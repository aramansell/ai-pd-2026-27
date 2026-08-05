#!/usr/bin/env bash
# ============================================================
#  AI Teacher Workbench - start (macOS / Linux)
#  Run:   ./run.sh
#  Then open http://localhost:5000
# ============================================================
set -e
cd "$(dirname "$0")"

# Friendly reminder if setup was skipped
if [ ! -f ".env" ]; then
  echo "No .env found. Run ./setup.sh first."
  exit 1
fi

# Use the venv if it exists, else fall back to system python.
if [ -d ".venv" ]; then
  PY=.venv/bin/python
else
  PY=python3
fi

echo "Starting AI Teacher Workbench ..."
echo "Press Ctrl+C to stop it."
echo ""
exec "$PY" app.py
