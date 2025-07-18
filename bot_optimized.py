import os
import json
import re
import asyncio
import aiofiles
import aiofiles.os
from typing import Dict, Optional
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from telegram.request import HTTPXRequest
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# File to store post numbers and links
LINKS_FILE = "links.json"

class LinkCache:
    """In-memory cache for links with async file operations"""
    
    def __init__(self):
        self._cache: Dict[str, str] = {}
        self._last_modified: Optional[float] = None
        self._lock = asyncio.Lock()
        self._initialized = False
    
    async def _should_refresh(self) -> bool:
        """Check if cache should be refreshed"""
        if not self._initialized:
            return True
        
        try:
            if await aiofiles.os.path.exists(LINKS_FILE):
                stat = await aiofiles.os.stat(LINKS_FILE)
                return stat.st_mtime != self._last_modified
        except Exception as e:
            logger.error(f"Error checking file modification time: {e}")
        
        return False
    
    async def _refresh_cache(self):
        """Refresh cache from file"""
        try:
            if await aiofiles.os.path.exists(LINKS_FILE):
                async with aiofiles.open(LINKS_FILE, "r") as f:
                    content = await f.read()
                    self._cache = json.loads(content) if content.strip() else {}
                
                stat = await aiofiles.os.stat(LINKS_FILE)
                self._last_modified = stat.st_mtime
            else:
                self._cache = {}
                self._last_modified = None
            
            self._initialized = True
            logger.info(f"Cache refreshed with {len(self._cache)} links")
        
        except Exception as e:
            logger.error(f"Error refreshing cache: {e}")
            if not self._initialized:
                self._cache = {}
                self._initialized = True
    
    async def get_links(self) -> Dict[str, str]:
        """Get all links (cached)"""
        async with self._lock:
            if await self._should_refresh():
                await self._refresh_cache()
            return self._cache.copy()
    
    async def get_link(self, post_number: str) -> Optional[str]:
        """Get a specific link by post number"""
        links = await self.get_links()
        return links.get(post_number)
    
    async def add_link(self, post_number: str, url: str):
        """Add a new link and update cache"""
        async with self._lock:
            # Update cache
            self._cache[post_number] = url
            
            # Save to file
            try:
                async with aiofiles.open(LINKS_FILE, "w") as f:
                    await f.write(json.dumps(self._cache, indent=2))
                
                # Update modification time
                stat = await aiofiles.os.stat(LINKS_FILE)
                self._last_modified = stat.st_mtime
                
                logger.info(f"Added link for post {post_number}")
            
            except Exception as e:
                logger.error(f"Error saving links: {e}")
                # Remove from cache if save failed
                self._cache.pop(post_number, None)
                raise

# Global cache instance
link_cache = LinkCache()

# Metrics collection
class MetricsCollector:
    def __init__(self):
        self.request_count = {"get_post": 0, "add_link": 0, "start": 0}
        self.response_times = []
        self.start_time = datetime.now()
    
    def record_request(self, command: str, duration: float):
        self.request_count[command] = self.request_count.get(command, 0) + 1
        self.response_times.append(duration)
        
        # Keep only last 1000 response times to prevent memory leak
        if len(self.response_times) > 1000:
            self.response_times = self.response_times[-1000:]
    
    def get_stats(self) -> Dict:
        avg_response_time = sum(self.response_times) / len(self.response_times) if self.response_times else 0
        uptime = (datetime.now() - self.start_time).total_seconds()
        
        return {
            "total_requests": sum(self.request_count.values()),
            "requests_by_command": self.request_count,
            "avg_response_time_ms": round(avg_response_time * 1000, 2),
            "uptime_seconds": round(uptime, 2)
        }

metrics = MetricsCollector()

# Decorator for timing requests
def timed_request(command_name: str):
    def decorator(func):
        async def wrapper(*args, **kwargs):
            start_time = asyncio.get_event_loop().time()
            try:
                result = await func(*args, **kwargs)
                return result
            finally:
                duration = asyncio.get_event_loop().time() - start_time
                metrics.record_request(command_name, duration)
        return wrapper
    return decorator

# Start command
@timed_request("start")
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Hello! Use /postno0001 to get a link!")

# Handle post number requests - OPTIMIZED: Single handler with pattern matching
@timed_request("get_post")
async def get_post(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        command = update.message.text.lower()
        match = re.match(r'/postno(\d{4})', command)
        if not match:
            await update.message.reply_text("❌ Invalid format. Use /postno0001.")
            return

        postno = match.group(1)
        
        # Use cached lookup instead of file I/O
        link = await link_cache.get_link(postno)
        
        if link:
            await update.message.reply_text(f"🔗 Link for post {postno}: {link}")
        else:
            await update.message.reply_text(f"❌ Post {postno} not found.")
    
    except Exception as e:
        logger.error(f"Error in get_post: {e}")
        await update.message.reply_text("❌ An error occurred. Please try again.")

# Admin-only command to add links
ADMIN_ID = 7655961867  # 🔁 Replace with your Telegram user ID

@timed_request("add_link")
async def add_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user_id = update.message.from_user.id
        if user_id != ADMIN_ID:
            await update.message.reply_text("⛔ Only the bot admin can add links.")
            return

        args = context.args
        if len(args) != 2:
            await update.message.reply_text("Usage: /addlink 0001 https://your-link")
            return

        postno, url = args
        
        # Validate post number format
        if not re.match(r'^\d{4}$', postno):
            await update.message.reply_text("❌ Post number must be 4 digits (e.g., 0001)")
            return
        
        # Validate URL format (basic validation)
        if not url.startswith(('http://', 'https://')):
            await update.message.reply_text("❌ URL must start with http:// or https://")
            return
        
        await link_cache.add_link(postno, url)
        await update.message.reply_text(f"✅ Saved link for post {postno}!")
    
    except Exception as e:
        logger.error(f"Error in add_link: {e}")
        await update.message.reply_text("❌ An error occurred while saving the link.")

# Health check endpoint
async def health_check(update: Update, context: ContextTypes.DEFAULT_TYPE):
    stats = metrics.get_stats()
    cache_size = len(link_cache._cache)
    
    health_info = (
        f"✅ Bot is healthy\n"
        f"📊 Total requests: {stats['total_requests']}\n"
        f"⏱️ Avg response time: {stats['avg_response_time_ms']}ms\n"
        f"🔗 Cached links: {cache_size}\n"
        f"⏰ Uptime: {stats['uptime_seconds']}s"
    )
    
    await update.message.reply_text(health_info)

# Stats command (admin only)
async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    if user_id != ADMIN_ID:
        await update.message.reply_text("⛔ Only the bot admin can view stats.")
        return
    
    stats_data = metrics.get_stats()
    cache_size = len(link_cache._cache)
    
    stats_info = (
        f"📊 **Bot Statistics**\n"
        f"Total requests: {stats_data['total_requests']}\n"
        f"Requests by command:\n"
    )
    
    for cmd, count in stats_data['requests_by_command'].items():
        stats_info += f"  • {cmd}: {count}\n"
    
    stats_info += (
        f"Average response time: {stats_data['avg_response_time_ms']}ms\n"
        f"Cached links: {cache_size}\n"
        f"Uptime: {stats_data['uptime_seconds']}s"
    )
    
    await update.message.reply_text(stats_info)

# Main function
async def main():
    try:
        token = os.environ.get("BOT_TOKEN")
        if not token:
            raise ValueError("BOT_TOKEN not set in environment variables.")

        # Optimized HTTP client with connection pooling
        request = HTTPXRequest(
            connection_pool_size=8,
            read_timeout=10,
            write_timeout=10,
            connect_timeout=5
        )

        app = ApplicationBuilder().token(token).request(request).build()

        # Add command handlers
        app.add_handler(CommandHandler("start", start))
        app.add_handler(CommandHandler("addlink", add_link))
        app.add_handler(CommandHandler("health", health_check))
        app.add_handler(CommandHandler("stats", stats))

        # OPTIMIZED: Single pattern-based handler instead of 10,000 individual handlers
        app.add_handler(MessageHandler(filters.Regex(r'^/postno\d{4}$'), get_post))

        # Initialize cache on startup
        logger.info("Initializing link cache...")
        await link_cache.get_links()
        logger.info("Cache initialized successfully")

        logger.info("Bot started successfully")
        await app.run_polling()
    
    except Exception as e:
        logger.error(f"Error starting bot: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(main())