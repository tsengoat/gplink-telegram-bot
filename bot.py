import os
import json
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import re

# File to store post numbers and links
LINKS_FILE = "links.json"

# Load or create the JSON file
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
    
    # Validate format
    if not re.fullmatch(r"\d{4}", postno):
        await update.message.reply_text("❌ Invalid post number format. Use 4 digits like /postno0001.")
        return

    links = load_links()
    
    if postno in links:
        await update.message.reply_text(f"🔗 Link for post {postno}: {links[postno]}")
    else:
        await update.message.reply_text(f"❌ Post {postno} not found.")

# Add post (admin-only)
ADMIN_ID = 7655961867  # ← replace with **your own Telegram user ID**

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
    application = ApplicationBuilder().token(os.environ['BOT_TOKEN']).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("addlink", add_link))
    
    for i in range(10000):
        command = f"postno{i:04}"
        application.add_handler(CommandHandler(command, get_post))

    application.run_polling()  # ← This is enough in v20+

if __name__ == "__main__":
    main()
