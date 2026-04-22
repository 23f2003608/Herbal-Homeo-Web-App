@echo off
cd /d "%~dp0"
set "PYTHON=python"
where python >nul 2>&1
if errorlevel 1 (
    where py >nul 2>&1
    if errorlevel 1 (
        echo Python not found. Please install Python 3.11 or later on this PC.
        pause
        exit /b 1
    )
    set "PYTHON=py"
)

if not exist venv\Scripts\activate (
    echo Creating portable virtual environment...
    %PYTHON% -m venv venv
)

call venv\Scripts\activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python run.py
