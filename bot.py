import os
import json
import re
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# File to store post numbers and links
LINKS_FILE = "links.json"

def load_links():
    if os.path.exists(LINKS_FILE):
        with open(LINKS_FILE, "r") as f:
            return json.load(f)
    return {}

def save_links(links):
    with open(LINKS_FILE, "w") as f:
        json.dump(links, f)

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Hello! Send /postno0001 to get a link!")

# Handle /postnoXXXX
async def get_post(update: Update, context: ContextTypes.DEFAULT_TYPE):
    postno = update.message.text.lower().replace("/postno", "")
    
    if not re.fullmatch(r"\d{4}", postno):
        await update.message.reply_text("❌ Invalid post number format. Use 4 digits like /postno0001.")
        return

    links = load_links()
    
    if postno in links:
        await update.message.reply_text(f"🔗 Link for post {postno}: {links[postno]}")
    else:
        await update.message.reply_text(f"❌ Post {postno} not found.")

# Add post (admin-only)
ADMIN_ID = 7655961867  # Replace with your actual Telegram ID

async def add_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id

    if user_id != ADMIN_ID:
        await update.message.reply_text("⛔ Only the bot owner can add links.")
        return

    args = context.args
    if len(args) != 2:
        await update.message.reply_text("Usage: /addlink 0001 https://your-link")
        return

    postno, link = args
    links = load_links()
    links[postno] = link
    save_links(links)

    await update.message.reply_text(f"✅ Saved link for post {postno}!")

# Main function
def main():
    token = os.environ.get("BOT_TOKEN")
    application = ApplicationBuilder().token(token).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("addlink", add_link))

    # Handle /postno0001 to /postno9999
    for i in range(10000):
        command = f"postno{i:04}"
        application.add_handler(CommandHandler(command, get_post))

    application.run_polling()

if __name__ == "__main__":
    main()
