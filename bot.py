import json
import re
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Replace this with your actual Telegram user ID (to restrict who can add links)
ALLOWED_ADMINS = [7655961867]  

DATA_FILE = 'links.json'

# Load existing links from file or start with empty dict
try:
    with open(DATA_FILE, 'r') as f:
        links = json.load(f)
except FileNotFoundError:
    links = {}

def save_links():
    with open(DATA_FILE, 'w') as f:
        json.dump(links, f)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Welcome! Send me a GPLink video URL to add it (admins only). "
        "Users can get links by sending commands like /postno0001."
    )

async def add_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    text = update.message.text.strip()

    if user_id not in ALLOWED_ADMINS:
        await update.message.reply_text("Sorry, you are not authorized to add links.")
        return

    # Check if the message is a valid GPLink URL (basic check)
    if not text.startswith('https://gplink.in/'):
        await update.message.reply_text("Please send a valid GPLink URL starting with https://gplink.in/")
        return

    # Find next post number
    if links:
        max_post = max(int(k) for k in links.keys())
        next_post = max_post + 1
    else:
        next_post = 1

    post_str = str(next_post).zfill(4)  # e.g. 0001

    links[post_str] = text
    save_links()

    await update.message.reply_text(f"Link added as post number {post_str}.")

async def get_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message.text.lower()
    match = re.match(r'/postno(\d{4})', message)
    if not match:
        await update.message.reply_text("Invalid command format. Use /postno0001")
        return

    post_no = match.group(1)
    link = links.get(post_no)

    if link:
        await update.message.reply_text(f"Post {post_no}: {link}")
    else:
        await update.message.reply_text(f"No link found for post number {post_no}.")

def main():
    # Replace 'YOUR_BOT_TOKEN_HERE' with your Telegram bot token
    application = ApplicationBuilder().token('8184783225:AAHzxB5YSb5dlIy-rmVYmZsXwTPaY0bopIc').build()

    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, add_link))
    application.add_handler(MessageHandler(filters.Regex(r'^/postno\d{4}$'), get_link))

    application.run_polling()

if __name__ == '__main__':
    main()
