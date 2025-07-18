import os
import json
import re
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# File to store post numbers and links
LINKS_FILE = "links.json"

# Load links from file
def load_links():
    if os.path.exists(LINKS_FILE):
        with open(LINKS_FILE, "r") as f:
            return json.load(f)
    return {}

# Save links to file
def save_links(links):
    with open(LINKS_FILE, "w") as f:
        json.dump(links, f, indent=2)

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_message = """
🤖 **GP Link Telegram Bot**

Welcome! This bot helps you share GP links to earn money.

**Commands:**
• `/postnumber00001` - Get link for post number 00001
• `/postnumber00002` - Get link for post number 00002
• ... and so on up to `/postnumber10000`

**Admin Commands:**
• `/addlink 00001 https://your-gplink.com` - Add a new link
• `/removelink 00001` - Remove a link
• `/listlinks` - Show all available links

**Format:** Use exactly `/postnumber` followed by 5 digits (00001-10000)

Start by typing `/postnumber00001` to test!
    """
    await update.message.reply_text(welcome_message, parse_mode='Markdown')

# Handle post number requests
async def handle_post_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    command = update.message.text.lower()
    
    # Match /postnumber followed by exactly 5 digits
    match = re.match(r'/postnumber(\d{5})', command)
    if not match:
        await update.message.reply_text(
            "❌ Invalid format!\n\n"
            "Use: `/postnumber00001` to `/postnumber10000`\n"
            "Example: `/postnumber00001`",
            parse_mode='Markdown'
        )
        return

    post_number = match.group(1)
    post_int = int(post_number)
    
    # Check if post number is in valid range (1-10000)
    if post_int < 1 or post_int > 10000:
        await update.message.reply_text(
            "❌ Post number must be between 00001 and 10000!\n"
            "Example: `/postnumber00001`",
            parse_mode='Markdown'
        )
        return

    links = load_links()

    if post_number in links:
        link = links[post_number]
        message = f"""
🔗 **Post Number: {post_number}**

💰 **Your GP Link:**
{link}

📱 Click the link above to start earning!
        """
        await update.message.reply_text(message, parse_mode='Markdown')
    else:
        await update.message.reply_text(
            f"❌ **Post {post_number} not found!**\n\n"
            f"This post number doesn't have a link yet.\n"
            f"Contact the admin to add links for post {post_number}.",
            parse_mode='Markdown'
        )

# Admin-only command to add links
ADMIN_ID = 7655961867  # Replace with your Telegram user ID

async def add_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    if user_id != ADMIN_ID:
        await update.message.reply_text("⛔ Only the bot admin can add links.")
        return

    args = context.args
    if len(args) != 2:
        await update.message.reply_text(
            "**Usage:** `/addlink 00001 https://your-gplink.com`\n\n"
            "**Example:** `/addlink 00001 https://gplinks.in/xyz123`",
            parse_mode='Markdown'
        )
        return

    post_number, link = args
    
    # Validate post number format
    if not re.match(r'^\d{5}$', post_number):
        await update.message.reply_text(
            "❌ Post number must be exactly 5 digits!\n"
            "Example: `00001`, `00123`, `10000`",
            parse_mode='Markdown'
        )
        return
    
    post_int = int(post_number)
    if post_int < 1 or post_int > 10000:
        await update.message.reply_text(
            "❌ Post number must be between 00001 and 10000!"
        )
        return

    # Validate URL
    if not (link.startswith('http://') or link.startswith('https://')):
        await update.message.reply_text(
            "❌ Please provide a valid URL starting with http:// or https://"
        )
        return

    links = load_links()
    links[post_number] = link
    save_links(links)

    await update.message.reply_text(
        f"✅ **Link saved successfully!**\n\n"
        f"**Post Number:** {post_number}\n"
        f"**Link:** {link}\n\n"
        f"Users can now use `/postnumber{post_number}` to get this link!",
        parse_mode='Markdown'
    )

# Admin command to remove links
async def remove_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    if user_id != ADMIN_ID:
        await update.message.reply_text("⛔ Only the bot admin can remove links.")
        return

    args = context.args
    if len(args) != 1:
        await update.message.reply_text(
            "**Usage:** `/removelink 00001`",
            parse_mode='Markdown'
        )
        return

    post_number = args[0]
    links = load_links()

    if post_number in links:
        del links[post_number]
        save_links(links)
        await update.message.reply_text(
            f"✅ **Link removed!**\n\n"
            f"Post number {post_number} has been removed.",
            parse_mode='Markdown'
        )
    else:
        await update.message.reply_text(
            f"❌ Post number {post_number} not found!"
        )

# Admin command to list all links
async def list_links(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    if user_id != ADMIN_ID:
        await update.message.reply_text("⛔ Only the bot admin can view all links.")
        return

    links = load_links()
    
    if not links:
        await update.message.reply_text("📝 No links found!")
        return

    message = "📝 **All Available Links:**\n\n"
    for post_number, link in sorted(links.items()):
        message += f"• Post {post_number}: {link[:50]}{'...' if len(link) > 50 else ''}\n"
    
    message += f"\n**Total:** {len(links)} links"
    
    await update.message.reply_text(message, parse_mode='Markdown')

# Main function
def main():
    token = os.environ.get("BOT_TOKEN")
    if not token:
        print("❌ BOT_TOKEN not set in environment variables.")
        print("Please set your bot token:")
        print("export BOT_TOKEN='your_bot_token_here'")
        return

    app = ApplicationBuilder().token(token).build()

    # Add command handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("addlink", add_link))
    app.add_handler(CommandHandler("removelink", remove_link))
    app.add_handler(CommandHandler("listlinks", list_links))
    
    # Handle all /postnumber messages
    app.add_handler(MessageHandler(
        filters.Regex(r'^/postnumber\d+'), 
        handle_post_request
    ))

    print("🤖 Bot is starting...")
    print("✅ Bot is running! Press Ctrl+C to stop.")
    app.run_polling()

if __name__ == "__main__":
    main()
