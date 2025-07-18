import os
import json
import re
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

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
    await update.message.reply_text("👋 Hello! Use /postno0001 to get a link!")

# Retrieve post number
async def get_post(update: Update, context: ContextTypes.DEFAULT_TYPE):
    postno = update.message.text.lower().replace("/postno", "")
    
    if not re.fullmatch(r"\d{4}", postno):
        await update.message.reply_text("❌ Invalid post number. Use format like /postno0001.")
        return

    links = load_links()
    if postno in links:
        await update.message.reply_text(f"🔗 Link for post {postno}: {links[postno]}")
    else:
        await update.message.reply_text("🚫 Link not found.")

# Only for admin to add links
ADMIN_ID = 7655961867  # 👈 Replace this with your Telegram user ID

async def add_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.from_user.id != ADMIN_ID:
        await update.message.reply_text("⛔ Only the admin can add links.")
        return

    if len(context.args) != 2:
        await update.message.reply_text("❗ Usage: /addlink 0001 https://example.com")
        return

    postno, link = context.args
    links = load_links()
    links[postno] = link
    save_links(links)
    await update.message.reply_text(f"✅ Saved link for post {postno}!")

def main():
    application = ApplicationBuilder().token(os.environ['BOT_TOKEN']).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("addlink", add_link))

    # Add handlers for /postnoXXXX
    for i in range(10000):
        command = f"postno{i:04}"
        application.add_handler(CommandHandler(command, get_post))

    application.run_polling()

if __name__ == "__main__":
    main()
