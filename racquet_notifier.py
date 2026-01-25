"""
Racquet Channel Notifier
Automatically posts new sale racquets to a Telegram channel.
Run this script periodically (e.g., via cron or launchd) to check for new deals.

SETUP:
1. Create a Telegram channel
2. Add your bot (@cheappoBot) as an admin to the channel
3. Get the channel ID:
   - Forward any message from your channel to @userinfobot
   - Or use the channel username like "@YourChannelName"
4. Set the CHANNEL_ID below
5. Run this script: python racquet_notifier.py

AUTOMATED SCHEDULING:
- macOS: Use launchd or cron
- Linux: Use cron
- Example cron (every 6 hours): 0 */6 * * * cd /path/to/cheappo && ./myenv/bin/python racquet_notifier.py
"""

import asyncio
import os
from telegram import Bot
from telegram.constants import ParseMode
from config import TOKEN
from scrapers.sunriseclick import get_new_sale_racquets, scrape_sale_racquets, format_racquet_message

# ============================================
# CONFIGURE YOUR CHANNEL ID HERE
# ============================================
# Option 1: Channel username (with @)
# CHANNEL_ID = "@YourChannelName"
#
# Option 2: Channel ID (numeric, starts with -100)
# CHANNEL_ID = "-1001234567890"
#
# Option 3: Environment variable
# CHANNEL_ID = os.environ.get("TELEGRAM_CHANNEL_ID", "")

CHANNEL_ID = os.environ.get("TELEGRAM_CHANNEL_ID", "-1003720624349")


async def send_to_channel(bot: Bot, message: str, image_url: str = None):
    """Send a message to the Telegram channel."""
    try:
        if image_url:
            # Send with image
            await bot.send_photo(
                chat_id=CHANNEL_ID,
                photo=image_url,
                caption=message,
                parse_mode=ParseMode.MARKDOWN
            )
        else:
            # Send text only
            await bot.send_message(
                chat_id=CHANNEL_ID,
                text=message,
                parse_mode=ParseMode.MARKDOWN
            )
        return True
    except Exception as e:
        print(f"Error sending to channel: {e}")
        return False


async def notify_new_racquets():
    """Check for new racquets and post them to the channel."""
    
    if not CHANNEL_ID:
        print("=" * 60)
        print("ERROR: CHANNEL_ID not set!")
        print("=" * 60)
        print("\nTo set up your channel:")
        print("1. Create a Telegram channel")
        print("2. Add your bot (@cheappoBot) as an admin")
        print("3. Get the channel ID:")
        print("   - Forward any message from your channel to @userinfobot")
        print("   - Or just use @YourChannelName")
        print("4. Edit racquet_notifier.py and set CHANNEL_ID")
        print("\nExample: CHANNEL_ID = \"@MyRacquetDeals\"")
        return
    
    print("Checking for new racquet deals...")
    
    # Get new racquets (only ones not seen before)
    new_racquets = get_new_sale_racquets()
    
    if not new_racquets:
        print("No new racquets found.")
        return
    
    print(f"Found {len(new_racquets)} new racquet(s)! Posting to channel...")
    
    # Initialize bot
    bot = Bot(token=TOKEN)
    
    # Post each racquet individually
    for i, racquet in enumerate(new_racquets, 1):
        message = (
            f"🏸 *NEW DEAL #{i}*\n\n"
            f"{format_racquet_message(racquet)}"
        )
        success = await send_to_channel(bot, message, racquet.get("image_url"))
        if success:
            print(f"  Posted: {racquet.get('title', 'Unknown')[:50]}...")
        await asyncio.sleep(1)  # Rate limiting to avoid Telegram limits
    
    print(f"\n✅ Successfully posted {len(new_racquets)} racquet(s) to channel!")


async def post_all_current_deals():
    """Post ALL current deals (not just new ones) - useful for initial channel setup."""
    
    if not CHANNEL_ID:
        print("ERROR: CHANNEL_ID not set! Edit racquet_notifier.py first.")
        return
    
    print("Fetching all current racquet deals...")
    racquets = scrape_sale_racquets()
    
    if not racquets:
        print("No racquets found.")
        return
    
    print(f"Found {len(racquets)} racquet(s). Posting to channel...")
    
    bot = Bot(token=TOKEN)
    
    # Post header
    header = (
        f"🏸 *BADMINTON RACQUET SALE* 🏸\n\n"
        f"Found {len(racquets)} racquet(s) with ≥10% discount!\n"
        f"Source: SunriseClick Singapore\n"
        f"━━━━━━━━━━━━━━━━━━━━"
    )
    await send_to_channel(bot, header)
    await asyncio.sleep(1)
    
    # Post each racquet (limit to avoid flooding)
    max_posts = 20  # Limit for initial post to avoid spam
    for i, racquet in enumerate(racquets[:max_posts], 1):
        message = format_racquet_message(racquet)
        await send_to_channel(bot, message, racquet.get("image_url"))
        print(f"  [{i}/{min(len(racquets), max_posts)}] Posted: {racquet.get('title', 'Unknown')[:40]}...")
        await asyncio.sleep(1)
    
    if len(racquets) > max_posts:
        footer = f"... and {len(racquets) - max_posts} more deals! Use /racquets in the bot to see all."
        await send_to_channel(bot, footer)
    
    print("\n✅ Done!")


def main():
    import sys
    
    print("=" * 60)
    print("🏸 Racquet Channel Notifier")
    print("=" * 60)
    
    if len(sys.argv) > 1 and sys.argv[1] == "--all":
        # Post all current deals (for initial channel setup)
        print("Mode: Posting ALL current deals\n")
        asyncio.run(post_all_current_deals())
    elif len(sys.argv) > 1 and sys.argv[1] == "--test":
        # Test mode - just check without posting
        print("Mode: Test (checking for deals without posting)\n")
        racquets = scrape_sale_racquets()
        print(f"Found {len(racquets)} racquets on sale")
        new_racquets = get_new_sale_racquets()
        print(f"Of those, {len(new_racquets)} are new (not seen before)")
    else:
        # Normal mode - post only new deals
        print("Mode: New deals only\n")
        asyncio.run(notify_new_racquets())


if __name__ == "__main__":
    main()
