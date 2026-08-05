#!/usr/bin/env bash
# ============================================================
#  AI Teacher Workbench - one-time setup (macOS / Linux)
#  Run once:   ./setup.sh
#  Then run:   ./run.sh
# ============================================================
set -e

cd "$(dirname "$0")"

echo "=============================================="
echo "  AI Teacher Workbench - setup (macOS/Linux)"
echo "=============================================="

# 1. Check Python
if ! command -v python3 >/dev/null 2>&1; then
  echo "ERROR: Python 3 is not installed."
  echo "  macOS: install from https://www.python.org/downloads/"
  echo "  Linux: use your package manager, e.g.  sudo apt install python3 python3-venv python3-pip"
  exit 1
fi
echo "[1/4] Python found: $(python3 --version)"

# 2. Create a virtual environment
if [ ! -d ".venv" ]; then
  echo "[2/4] Creating a virtual environment (.venv) ..."
  python3 -m venv .venv
else
  echo "[2/4] Virtual environment already exists (.venv)."
fi

# 3. Install dependencies
echo "[3/4] Installing Python libraries (this may take a minute) ..."
./.venv/bin/python -m pip install --upgrade pip >/dev/null
./.venv/bin/python -m pip install -r requirements.txt

# 4. Create .env if needed
if [ ! -f ".env" ]; then
  echo "[4/4] Creating your .env from the template ..."
  cp .env.example .env
  echo "  -> Open .env in a text editor to choose your AI provider."
else
  echo "[4/4] .env already exists. Leaving it alone."
fi

echo ""
echo "Setup complete."
echo ""
echo "Next steps:"
echo "  1. Decide your AI provider:"
echo "     - Free/offline: install Ollama and pull a model (see SETUP.md)."
echo "     - Cloud:        get a free key at ollama.com/signup, put it in .env."
echo "  2. Start the app:   ./run.sh"
echo "  3. Open:            http://localhost:5000"
echo ""
