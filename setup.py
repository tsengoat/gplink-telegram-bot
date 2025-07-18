#!/usr/bin/env python3
"""
Setup script for GP Link Telegram Bot
This script helps you configure and run the bot easily.
"""

import os
import sys
import json
import subprocess

def print_header():
    print("=" * 60)
    print("🤖 GP Link Telegram Bot Setup")
    print("=" * 60)
    print()

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 7):
        print("❌ Python 3.7 or higher is required!")
        print(f"Current version: {sys.version}")
        sys.exit(1)
    print(f"✅ Python version: {sys.version.split()[0]}")

def install_dependencies():
    """Install required Python packages"""
    print("\n📦 Installing dependencies...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                      check=True, capture_output=True)
        print("✅ Dependencies installed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        sys.exit(1)

def get_bot_token():
    """Get bot token from user"""
    print("\n🔑 Bot Token Configuration")
    print("1. Go to @BotFather on Telegram")
    print("2. Send /newbot and follow instructions")
    print("3. Copy the bot token")
    print()
    
    token = input("Enter your bot token: ").strip()
    if not token:
        print("❌ Bot token cannot be empty!")
        sys.exit(1)
    
    return token

def get_admin_id():
    """Get admin user ID"""
    print("\n👤 Admin Configuration")
    print("1. Go to @userinfobot on Telegram")
    print("2. Send /start to get your user ID")
    print("3. Copy your user ID (numbers only)")
    print()
    
    while True:
        admin_id = input("Enter your Telegram user ID: ").strip()
        if admin_id.isdigit():
            return int(admin_id)
        print("❌ Please enter only numbers!")

def update_admin_id(admin_id):
    """Update admin ID in bot.py"""
    try:
        with open('bot.py', 'r') as f:
            content = f.read()
        
        # Replace the admin ID
        import re
        updated_content = re.sub(
            r'ADMIN_ID = \d+',
            f'ADMIN_ID = {admin_id}',
            content
        )
        
        with open('bot.py', 'w') as f:
            f.write(updated_content)
        
        print(f"✅ Admin ID updated to: {admin_id}")
    except Exception as e:
        print(f"❌ Failed to update admin ID: {e}")
        sys.exit(1)

def set_environment_variable(token):
    """Set environment variable for bot token"""
    print("\n🔧 Setting environment variable...")
    
    # For current session
    os.environ['BOT_TOKEN'] = token
    
    # Create a .env file for future use
    try:
        with open('.env', 'w') as f:
            f.write(f"BOT_TOKEN={token}\n")
        print("✅ Environment variable set!")
        print("📝 Token saved to .env file")
    except Exception as e:
        print(f"⚠️ Could not create .env file: {e}")
        print("You may need to set BOT_TOKEN manually")

def create_sample_links():
    """Create sample links for testing"""
    print("\n📝 Creating sample links...")
    
    sample_links = {
        "00001": "https://gplinks.in/sample1",
        "00002": "https://gplinks.in/sample2",
        "00003": "https://gplinks.in/sample3"
    }
    
    try:
        with open('links.json', 'w') as f:
            json.dump(sample_links, f, indent=2)
        print("✅ Sample links created!")
        print("   - /postnumber00001")
        print("   - /postnumber00002") 
        print("   - /postnumber00003")
    except Exception as e:
        print(f"⚠️ Could not create sample links: {e}")

def run_bot():
    """Ask user if they want to run the bot"""
    print("\n🚀 Setup Complete!")
    print("=" * 60)
    print("Your bot is ready to use!")
    print()
    print("Commands available:")
    print("  For users: /postnumber00001 to /postnumber10000")
    print("  For admin: /addlink, /removelink, /listlinks")
    print()
    
    choice = input("Do you want to start the bot now? (y/n): ").strip().lower()
    if choice in ['y', 'yes']:
        print("\n🤖 Starting bot...")
        print("Press Ctrl+C to stop the bot")
        print("-" * 40)
        try:
            subprocess.run([sys.executable, "bot.py"])
        except KeyboardInterrupt:
            print("\n👋 Bot stopped!")
    else:
        print("\n📋 To start the bot later, run:")
        print("   python bot.py")
        print("\n💡 Don't forget to set BOT_TOKEN environment variable!")

def main():
    """Main setup function"""
    print_header()
    
    # Check Python version
    check_python_version()
    
    # Install dependencies
    install_dependencies()
    
    # Get configuration
    token = get_bot_token()
    admin_id = get_admin_id()
    
    # Update configuration
    update_admin_id(admin_id)
    set_environment_variable(token)
    
    # Create sample data
    create_sample_links()
    
    # Run bot
    run_bot()

if __name__ == "__main__":
    main()