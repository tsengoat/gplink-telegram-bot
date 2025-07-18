#!/usr/bin/env python3
"""Telegram gplink bot – public /postnoXXXX command, admin-only /upload.

Features
--------
1. Anyone can send `/postno00042` (any 1–5-digit number) and receive the link.
2. Admin(s) can override a link with `/upload <postNo> <url>` – stored persistently.
3. No per-number handlers – one regex handles everything.
4. Runs on Render free tier with python-telegram-bot 20+.
"""
from __future__ import annotations

import json
import logging
import os
import re
from pathlib import Path

from telegram import Update
from telegram.ext import (
    Application,
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

# ----------------------------- CONFIG ----------------------------------
BOT_TOKEN = os.getenv("BOT_TOKEN")  # set in Render environment
ADMIN_IDS = {
    int(x) for x in os.getenv("ADMIN_IDS", "").split(",") if x.strip().isdigit()
}  # comma-sep list of admin user-ids
BASE_URL = os.getenv("BASE_URL", "https://gplink.com/post/")
MAX_POST = int(os.getenv("MAX_POST", "10000"))
DATA_FILE = Path("links.json")  # persistent storage inside Render disk
# -----------------------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
logger = logging.getLogger(__name__)

# Cache links in memory for speed
try:
    LINKS: dict[int, str] = {int(k): v for k, v in json.loads(DATA_FILE.read_text()).items()}
except Exception:
    LINKS = {}

# ------------------------- Helpers -------------------------------------

def save_links() -> None:
    """Persist LINKS cache to JSON file."""
    try:
        DATA_FILE.write_text(json.dumps({str(k): v for k, v in LINKS.items()}, indent=2))
    except Exception as exc:
        logger.error("Failed to save links.json: %s", exc)


def make_link(n: int) -> str:
    """Return default link for a post number (5-digit zero-padded)."""
    return f"{BASE_URL}{n:05d}"


# ------------------------- Handlers ------------------------------------

POSTNO_RE = re.compile(r"^/postno(\d{1,5})$")  # up to 5 digits, leading zeros allowed


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Hi!\n" "• Anyone: /postno00001 → get link.\n" "• Admin: /upload <post> <url> → set link."
    )


async def postno(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    match = POSTNO_RE.match(update.message.text.strip())
    if not match:
        return  # regex handler guarantees this normally

    num = int(match.group(1).lstrip("0") or 0)
    if not (1 <= num <= MAX_POST):
        await update.message.reply_text(f"❌ Post must be 1–{MAX_POST}.")
        return

    link = LINKS.get(num, make_link(num))
    await update.message.reply_text(link)


async def upload(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    if user_id not in ADMIN_IDS:
        await update.message.reply_text("🚫 You are not authorised to upload.")
        return

    if len(context.args) != 2:
        await update.message.reply_text("Usage: /upload <postNumber> <full_url>")
        return

    try:
        num = int(context.args[0])
    except ValueError:
        await update.message.reply_text("First argument must be the post number (digits).")
        return

    if not (1 <= num <= MAX_POST):
        await update.message.reply_text(f"❌ Post must be 1–{MAX_POST}.")
        return

    url = context.args[1]
    LINKS[num] = url
    save_links()
    await update.message.reply_text(f"✅ Saved custom link for post {num:05d}.")


# Aliases for compatibility with dummy server thread
async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Alias to start() for backward compatibility."""
    await start(update, context)

async def handle_postno(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Alias to postno() for backward compatibility."""
    await postno(update, context)


# ---------------------------- Main -------------------------------------

def main() -> None:
    if not BOT_TOKEN:
        raise RuntimeError("BOT_TOKEN environment variable is missing.")

    application: Application = ApplicationBuilder().token(BOT_TOKEN).build()

    # Public commands
    application.add_handler(MessageHandler(filters.Regex(POSTNO_RE), postno))
    application.add_handler(CommandHandler("start", start))

    # Admin command
    application.add_handler(CommandHandler("upload", upload))

    logger.info("Bot starting …")
    application.run_polling()


if __name__ == "__main__":
    main()
