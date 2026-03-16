@echo off
cd /d "%~dp0"
echo.
echo   Starting Urban Survey Report Generator...
echo   http://localhost:5000
echo.
.venv\Scripts\python.exe run_app.py
pause
