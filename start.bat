@echo off
chcp 65001 >nul
set PYTHONIOENCODING=utf-8

cd /d "%~dp0"

python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python not found. Please install Python and add it to PATH.
    pause
    exit /b 1
)

if not exist main.py (
    echo [ERROR] main.py not found.
    pause
    exit /b 1
)

if not exist data\goals.json (
    echo [INFO] goals.json not found, will create new file.
)

echo [INFO] Starting MyTarget...
python main.py

if %errorlevel% neq 0 (
    echo [ERROR] Program exited with error.
    pause
    exit /b 1
)

exit /b 0 