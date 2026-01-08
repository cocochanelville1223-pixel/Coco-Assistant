@echo off
REM Coco Assistant Launcher for Windows
REM This script helps launch Coco Assistant with the appropriate interface

echo 🤖 Coco Assistant Launcher
echo ==========================

REM Activate virtual environment if it exists
if exist ".venv\Scripts\activate.bat" (
    echo ✓ Activating virtual environment...
    call .venv\Scripts\activate.bat
)

REM Check if we're in a GUI environment (basic check)
if "%SESSIONNAME%"=="Console" (
    echo ✓ Console detected - using text mode...
    python main.py
) else (
    echo ✓ GUI environment detected - attempting GUI mode...
    python main.py
)

pause