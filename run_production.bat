@echo off
echo ===================================================
echo 🚀 STARTING HR-AI SYSTEM (PRODUCTION MODE)
echo ===================================================

:: Check for Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python not found. Please install Python 3.8+
    pause
    exit /b 1
)

:: Setup Virtual Environment if not exists
if not exist "venv" (
    echo [INFO] Creating virtual environment...
    python -m venv venv
)

:: Activate Virtual Environment
echo [INFO] Activating virtual environment...
call venv\Scripts\activate

:: Install/Check Dependencies
echo [INFO] Checking dependencies...
pip install -r requirements.txt >nul 2>&1

:: Start the Enhanced System
echo [INFO] Starting System Components...
echo.
echo    1. Backend Server (Port 5000)
echo    2. Streamlit Dashboard (Port 8501)
echo    3. Monitoring & Backups
echo.
echo [INFO] System is starting up. Please wait...
echo.

python start_enhanced_system.py

pause
