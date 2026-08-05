@echo off
rem ============================================================
rem  AI Teacher Workbench - start (Windows)
rem  Run:   run.bat
rem  Then open http://localhost:5000
rem ============================================================
cd /d "%~dp0"

if not exist ".env" (
  echo No .env found. Run setup.bat first.
  pause
  exit /b 1
)

if exist ".venv\Scripts\python.exe" (
  set PY=.venv\Scripts\python.exe
) else (
  set PY=python
)

echo Starting AI Teacher Workbench ...
echo Press Ctrl+C to stop it.
echo.
"%PY%" app.py
pause
