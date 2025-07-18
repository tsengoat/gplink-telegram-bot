#!/bin/bash

# GP Link Telegram Bot Startup Script

echo "🤖 GP Link Telegram Bot"
echo "======================="

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Check if .env file exists and load it
if [ -f ".env" ]; then
    echo "📝 Loading environment variables from .env file..."
    export $(cat .env | xargs)
fi

# Check if BOT_TOKEN is set
if [ -z "$BOT_TOKEN" ]; then
    echo "❌ BOT_TOKEN is not set!"
    echo "Please run: export BOT_TOKEN='your_bot_token_here'"
    echo "Or create a .env file with BOT_TOKEN=your_bot_token_here"
    exit 1
fi

# Check if dependencies are installed
if ! python -c "import telegram" &> /dev/null; then
    echo "📦 Installing dependencies..."
    pip install -r requirements.txt
fi

echo "🚀 Starting bot..."
echo "Press Ctrl+C to stop"
echo "===================="

# Run the bot
python bot.py