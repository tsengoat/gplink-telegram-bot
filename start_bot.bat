@echo off
REM GP Link Telegram Bot Startup Script for Windows

echo 🤖 GP Link Telegram Bot
echo =======================

REM Check if .env file exists and load it
if exist .env (
    echo 📝 Loading environment variables from .env file...
    for /f "tokens=*" %%i in (.env) do set %%i
)

REM Check if BOT_TOKEN is set
if "%BOT_TOKEN%"=="" (
    echo ❌ BOT_TOKEN is not set!
    echo Please run: set BOT_TOKEN=your_bot_token_here
    echo Or create a .env file with BOT_TOKEN=your_bot_token_here
    pause
    exit /b 1
)

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed!
    pause
    exit /b 1
)

REM Check if dependencies are installed
python -c "import telegram" >nul 2>&1
if errorlevel 1 (
    echo 📦 Installing dependencies...
    pip install -r requirements.txt
)

echo 🚀 Starting bot...
echo Press Ctrl+C to stop
echo ====================

REM Run the bot
python bot.py

pause