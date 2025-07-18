#!/usr/bin/env python3
"""
Test script for GP Link Telegram Bot
This script tests the bot configuration without running the full bot.
"""

import os
import json
import sys

def test_python_version():
    """Test Python version compatibility"""
    print("🐍 Testing Python version...")
    if sys.version_info < (3, 7):
        print(f"❌ Python 3.7+ required, found {sys.version.split()[0]}")
        return False
    print(f"✅ Python {sys.version.split()[0]} - OK")
    return True

def test_dependencies():
    """Test if required dependencies are installed"""
    print("\n📦 Testing dependencies...")
    try:
        import telegram
        print("✅ python-telegram-bot - OK")
        return True
    except ImportError:
        print("❌ python-telegram-bot not installed")
        print("Run: pip install -r requirements.txt")
        return False

def test_bot_token():
    """Test if bot token is configured"""
    print("\n🔑 Testing bot token...")
    token = os.environ.get("BOT_TOKEN")
    if not token:
        print("❌ BOT_TOKEN not set in environment")
        return False
    
    if len(token) < 40:
        print("❌ BOT_TOKEN seems too short")
        return False
    
    print("✅ BOT_TOKEN is set")
    return True

def test_admin_id():
    """Test if admin ID is configured in bot.py"""
    print("\n👤 Testing admin ID...")
    try:
        with open('bot.py', 'r') as f:
            content = f.read()
        
        import re
        match = re.search(r'ADMIN_ID = (\d+)', content)
        if not match:
            print("❌ ADMIN_ID not found in bot.py")
            return False
        
        admin_id = int(match.group(1))
        if admin_id == 7655961867:  # Default value
            print("⚠️  ADMIN_ID is still default value")
            print("   Please update it with your Telegram user ID")
            return False
        
        print(f"✅ ADMIN_ID set to: {admin_id}")
        return True
    except Exception as e:
        print(f"❌ Error reading bot.py: {e}")
        return False

def test_file_structure():
    """Test if required files exist"""
    print("\n📁 Testing file structure...")
    required_files = ['bot.py', 'requirements.txt']
    all_good = True
    
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file} - OK")
        else:
            print(f"❌ {file} - Missing")
            all_good = False
    
    return all_good

def test_links_file():
    """Test links.json file"""
    print("\n📝 Testing links file...")
    if not os.path.exists('links.json'):
        print("⚠️  links.json doesn't exist (will be created automatically)")
        return True
    
    try:
        with open('links.json', 'r') as f:
            links = json.load(f)
        print(f"✅ links.json loaded - {len(links)} links found")
        return True
    except Exception as e:
        print(f"❌ Error reading links.json: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 GP Link Telegram Bot - Configuration Test")
    print("=" * 50)
    
    tests = [
        test_python_version,
        test_dependencies,
        test_bot_token,
        test_admin_id,
        test_file_structure,
        test_links_file
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} passed")
    
    if passed == total:
        print("🎉 All tests passed! Your bot is ready to run.")
        print("\nTo start the bot:")
        print("  Linux/Mac: ./start_bot.sh")
        print("  Windows:   start_bot.bat")
        print("  Manual:    python bot.py")
    else:
        print("⚠️  Some tests failed. Please fix the issues above.")
        print("\nFor help, check the README.md file.")

if __name__ == "__main__":
    main()