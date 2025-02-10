@echo off
chcp 65001 >nul
set PYTHONIOENCODING=utf-8

cd /d "%~dp0"

echo [INFO] Cleaning old build files...
rmdir /s /q build 2>nul
rmdir /s /q dist 2>nul
del /f /q *.spec 2>nul

echo [INFO] Starting build process...
python -m PyInstaller --clean ^
    --name MyTarget ^
    --icon "assets\mytarget.ico" ^
    --add-data "assets\*;assets" ^
    --add-data "data\*;data" ^
    --noconsole ^
    --onefile ^
    main.py

if %errorlevel% neq 0 (
    echo [ERROR] Build failed.
    pause
    exit /b 1
)

echo [INFO] Build completed successfully!
pause 