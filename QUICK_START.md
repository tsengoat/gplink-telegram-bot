# 🚀 Quick Start Guide - GP Link Telegram Bot

## Step-by-Step Setup (5 minutes)

### 1. Create Your Telegram Bot
1. Open Telegram and search for `@BotFather`
2. Send `/newbot` to BotFather
3. Choose a name: `GP Link Bot`
4. Choose a username: `gplink_earn_bot` (must be unique)
5. **Copy the bot token** (looks like: `1234567890:ABCdefGHIjklMNOpqrsTUVwxyz`)

### 2. Get Your User ID
1. Search for `@userinfobot` on Telegram
2. Send `/start` to get your user ID
3. **Copy your user ID** (a number like: `123456789`)

### 3. Configure the Bot
Open `bot.py` and change this line:
```python
ADMIN_ID = 7655961867  # Replace with your Telegram user ID
```

### 4. Set Your Bot Token
Create a `.env` file with your bot token:
```bash
echo "BOT_TOKEN=your_bot_token_here" > .env
```

### 5. Run the Bot
**Linux/Mac:**
```bash
./start_bot.sh
```

**Windows:**
```cmd
start_bot.bat
```

**Manual:**
```bash
source venv/bin/activate
python bot.py
```

## 🎯 Usage Examples

### For Users:
- `/start` - Get welcome message
- `/postnumber00001` - Get link for post 1
- `/postnumber00123` - Get link for post 123
- `/postnumber10000` - Get link for post 10000

### For Admin:
- `/addlink 00001 https://gplinks.in/xyz123` - Add a link
- `/removelink 00001` - Remove a link
- `/listlinks` - Show all links

## 💰 How to Earn Money

1. **Sign up** for GP link services:
   - gplinks.in
   - gplinks.co
   - shorte.st
   - linkvertise.com

2. **Create shortened links** for your content

3. **Add links to bot**:
   ```
   /addlink 00001 https://gplinks.in/abc123
   /addlink 00002 https://gplinks.co/def456
   ```

4. **Share your bot** with users

5. **Earn money** when users click the links!

## 🔧 Troubleshooting

**Bot not responding?**
- Check if BOT_TOKEN is correct
- Make sure bot is running
- Check if you're using the right username

**Can't add links?**
- Make sure you're the admin (check ADMIN_ID)
- Use correct format: `/addlink 00001 https://...`

**Invalid format error?**
- Use exactly 5 digits: `00001`, not `1`
- Use `/postnumber` not `/post` or `/link`

## 📱 Test Your Bot

1. Start the bot
2. Send `/start` to your bot
3. Try `/postnumber00001`
4. As admin, try `/addlink 00001 https://google.com`
5. Try `/postnumber00001` again

## 🎉 You're Ready!

Your GP Link Telegram Bot is now ready to help you earn money! Share your bot with friends and start earning from GP links.

**Bot Commands Summary:**
- Users: `/postnumber00001` to `/postnumber10000`
- Admin: `/addlink`, `/removelink`, `/listlinks`

**Happy earning! 💰**