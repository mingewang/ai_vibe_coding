@echo off
echo =========================================
echo Customer Service RAG Chatbot - Setup
echo =========================================
echo.

echo Step 1: Creating virtual environment...
if not exist ".venv" (
    python -m venv .venv
    if %errorlevel% neq 0 (
        echo Failed to create virtual environment. Make sure Python 3.10+ is installed.
        pause
        exit /b 1
    )
    echo   Virtual environment created.
) else (
    echo   Virtual environment already exists.
)

echo Step 2: Installing dependencies...
call .venv\Scripts\activate.bat
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo Failed to install dependencies.
    pause
    exit /b 1
)
echo   Dependencies installed.

echo.
echo Step 3: Setting up environment...
if not exist ".env" (
    copy .env.example .env
    echo   Created .env file. Please edit it with your API keys.
) else (
    echo   .env file already exists.
)

echo.
echo =========================================
echo Setup complete!
echo.
echo Next steps:
echo   1. Edit .env with your API keys
echo   2. Run: streamlit run app.py
echo =========================================
pause
