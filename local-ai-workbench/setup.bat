@echo off
rem ============================================================
rem  AI Teacher Workbench - one-time setup (Windows)
rem  Run once:   setup.bat
rem  Then run:   run.bat
rem ============================================================
cd /d "%~dp0"

echo ==============================================
echo   AI Teacher Workbench - setup (Windows)
echo ==============================================

rem 1. Check Python
python --version >nul 2>&1
if errorlevel 1 (
  echo ERROR: Python is not installed.
  echo   Install it from https://www.python.org/downloads/
  echo   IMPORTANT: tick "Add Python to PATH" during install.
  pause
  exit /b 1
)
echo [1/4] Python found.
python --version

rem 2. Create a virtual environment
if not exist ".venv" (
  echo [2/4] Creating a virtual environment (.venv) ...
  python -m venv .venv
) else (
  echo [2/4] Virtual environment already exists (.venv).
)

rem 3. Install dependencies
echo [3/4] Installing Python libraries (this may take a minute) ...
".venv\Scripts\python.exe" -m pip install --upgrade pip >nul
".venv\Scripts\python.exe" -m pip install -r requirements.txt

rem 4. Create .env if needed
if not exist ".env" (
  echo [4/4] Creating your .env from the template ...
  copy .env.example .env >nul
  echo   - Open .env in a text editor to choose your AI provider.
) else (
  echo [4/4] .env already exists. Leaving it alone.
)

echo.
echo Setup complete.
echo.
echo Next steps:
echo   1. Decide your AI provider:
echo      - Free/offline: install Ollama and pull a model (see SETUP.md).
echo      - Cloud:        get a free key at ollama.com/signup, put it in .env.
echo   2. Start the app:   run.bat
echo   3. Open:            http://localhost:5000
echo.
pause
