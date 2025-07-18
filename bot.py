import os
import json
import re
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# File to store post numbers and links
LINKS_FILE = "links.json"

# Load links from file (called once at startup)
def _load_links_from_disk() -> dict[str, str]:
    """Load the persistent links mapping from disk once at startup."""
    if os.path.exists(LINKS_FILE):
        with open(LINKS_FILE, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                # Corrupted file – start fresh rather than crashing
                return {}
    return {}


# Persist links to disk (called only when the mapping changes)
def _save_links_to_disk():
    with open(LINKS_FILE, "w") as f:
        json.dump(LINKS, f)


# Cache links in-memory to avoid disk I/O on every request
LINKS: dict[str, str] = _load_links_from_disk()

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Hello! Use /postno0001 to get a link!")

# Handle post number requests
async def get_post(update: Update, context: ContextTypes.DEFAULT_TYPE):
    command = update.message.text.lower()
    match = re.match(r'/postno(\d{4})', command)
    if not match:
        await update.message.reply_text("❌ Invalid format. Use /postno0001.")
        return

    postno = match.group(1)
    if postno in LINKS:
        await update.message.reply_text(f"🔗 Link for post {postno}: {LINKS[postno]}")
    else:
        await update.message.reply_text(f"❌ Post {postno} not found.")

# Admin-only command to add links
ADMIN_ID = 7655961867  # 🔁 Replace with your Telegram user ID

async def add_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    if user_id != ADMIN_ID:
        await update.message.reply_text("⛔ Only the bot admin can add links.")
        return

    args = context.args
    if len(args) != 2:
        await update.message.reply_text("Usage: /addlink 0001 https://your-link")
        return

    postno, link = args
    LINKS[postno] = link
    _save_links_to_disk()

    await update.message.reply_text(f"✅ Saved link for post {postno}!")

# Main function
def main():
    token = os.environ.get("BOT_TOKEN")
    if not token:
        raise ValueError("BOT_TOKEN not set in environment variables.")

    app = ApplicationBuilder().token(token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("addlink", add_link))

    # One regex-based handler covers every /postno#### command
    postno_regex = r"^/postno\d{4}$"
    app.add_handler(MessageHandler(filters.Regex(postno_regex), get_post))

    app.run_polling()

if __name__ == "__main__":
    main()
