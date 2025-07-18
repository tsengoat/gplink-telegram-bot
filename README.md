# 🤖 GP Link Telegram Bot

A Telegram bot that helps you share GP links to earn money. Users can request links by post numbers from 00001 to 10000.

## 📋 Features

- **Post Number Requests**: Users can get GP links using `/postnumber00001` to `/postnumber10000`
- **Admin Controls**: Add, remove, and list links
- **Data Persistence**: Links are saved in JSON format
- **Input Validation**: Proper validation for post numbers and URLs
- **User-Friendly**: Clear error messages and formatted responses

## 🚀 Quick Start

### Step 1: Create a Telegram Bot

1. Open Telegram and search for `@BotFather`
2. Send `/newbot` to BotFather
3. Choose a name for your bot (e.g., "GP Link Bot")
4. Choose a username for your bot (e.g., "gplink_earn_bot")
5. Copy the bot token (looks like: `1234567890:ABCdefGHIjklMNOpqrsTUVwxyz`)

### Step 2: Get Your Telegram User ID

1. Search for `@userinfobot` on Telegram
2. Send `/start` to get your user ID
3. Copy your user ID (a number like: `123456789`)

### Step 3: Configure the Bot

1. Open `bot.py` and replace `ADMIN_ID = 7655961867` with your user ID:
   ```python
   ADMIN_ID = 123456789  # Replace with your Telegram user ID
   ```

### Step 4: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 5: Set Environment Variable

**On Linux/Mac:**
```bash
export BOT_TOKEN='your_bot_token_here'
```

**On Windows:**
```cmd
set BOT_TOKEN=your_bot_token_here
```

### Step 6: Run the Bot

```bash
python bot.py
```

You should see:
```
🤖 Bot is starting...
✅ Bot is running! Press Ctrl+C to stop.
```

## 📱 How to Use

### For Users

1. Start the bot: `/start`
2. Get a link: `/postnumber00001` (replace 00001 with any number from 00001 to 10000)

### For Admins

1. **Add a link**: `/addlink 00001 https://gplinks.in/xyz123`
2. **Remove a link**: `/removelink 00001`
3. **List all links**: `/listlinks`

## 🔧 Configuration

### Changing Admin ID

Edit `bot.py` and change:
```python
ADMIN_ID = 7655961867  # Replace with your Telegram user ID
```

### Changing Post Number Range

Currently supports 00001-10000. To change:
1. Modify the validation in `handle_post_request()`
2. Update the regex pattern if needed

## 📁 File Structure

```
telegram-bot/
├── bot.py              # Main bot code
├── requirements.txt    # Python dependencies
├── links.json         # Stored links (auto-created)
└── README.md          # This file
```

## 🛠️ Troubleshooting

### Common Issues

1. **"BOT_TOKEN not set"**
   - Make sure you set the environment variable correctly
   - Check if the token is correct

2. **"Invalid format"**
   - Use exactly `/postnumber` followed by 5 digits
   - Example: `/postnumber00001`, not `/postnumber1`

3. **"Only the bot admin can add links"**
   - Make sure you set the correct ADMIN_ID in bot.py
   - Use your actual Telegram user ID

### Getting Help

1. Check the error messages in the terminal
2. Make sure all dependencies are installed
3. Verify your bot token is correct
4. Ensure you're using the correct command format

## 🔒 Security Notes

- Keep your bot token secret
- Only share admin access with trusted users
- Regularly backup your `links.json` file
- Monitor bot usage for abuse

## 📈 Earning Money

1. Sign up for GP link services (like gplinks.in, gplinks.co, etc.)
2. Shorten your links using these services
3. Add the shortened links to your bot using `/addlink`
4. Share your bot with users
5. Earn money when users click the links!

## 🔄 Updates

To update the bot:
1. Stop the bot (Ctrl+C)
2. Update the code
3. Restart the bot

## 📞 Support

If you need help:
1. Check this README first
2. Look at the error messages
3. Make sure all steps are followed correctly

---

**Happy earning! 💰**