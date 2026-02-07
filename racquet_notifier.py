"""
Racquet Channel Notifier
Automatically posts new sale racquets to a Telegram channel.
Monitors both Yonex (SunriseClick) and Li-Ning products.
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
from scrapers.sunriseclick import get_new_sale_racquets as get_new_yonex, scrape_sale_racquets as scrape_yonex, format_racquet_message as format_yonex_message
from scrapers.lining import get_new_sale_products as get_new_lining, scrape_sale_products as scrape_lining, format_product_message as format_lining_message

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

CHANNEL_ID = os.environ.get("TELEGRAM_CHANNEL_ID", "")


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
    """Check for new racquets from both Yonex and Li-Ning and post them to the channel."""
    
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
    
    print("Checking for new racquet deals from Yonex and Li-Ning...")
    
    # Get new products from both sources
    print("\n🏸 Checking Yonex (SunriseClick)...")
    new_yonex = get_new_yonex()
    print(f"  Found {len(new_yonex)} new Yonex racquet(s)")
    
    print("\n🏸 Checking Li-Ning...")
    new_lining = get_new_lining()
    print(f"  Found {len(new_lining)} new Li-Ning product(s)")
    
    total_new = len(new_yonex) + len(new_lining)
    
    if total_new == 0:
        print("\nNo new deals found from either source.")
        return
    
    print(f"\n✨ Total: {total_new} new deal(s)! Posting to channel...")
    
    # Initialize bot
    bot = Bot(token=TOKEN)
    
    # Post Yonex racquets
    if new_yonex:
        header = f"🏸 *YONEX - {len(new_yonex)} New Deal(s)*\n━━━━━━━━━━━━━━━━━━━━"
        await send_to_channel(bot, header)
        await asyncio.sleep(1)
        
        for i, racquet in enumerate(new_yonex, 1):
            message = format_yonex_message(racquet)
            success = await send_to_channel(bot, message, racquet.get("image_url"))
            if success:
                print(f"  [Yonex {i}/{len(new_yonex)}] Posted: {racquet.get('title', 'Unknown')[:50]}...")
            await asyncio.sleep(1)
    
    # Post Li-Ning products
    if new_lining:
        header = f"🏸 *LI-NING - {len(new_lining)} New Deal(s)*\n━━━━━━━━━━━━━━━━━━━━"
        await send_to_channel(bot, header)
        await asyncio.sleep(1)
        
        for i, product in enumerate(new_lining, 1):
            message = format_lining_message(product)
            success = await send_to_channel(bot, message, product.get("image_url"))
            if success:
                print(f"  [Li-Ning {i}/{len(new_lining)}] Posted: {product.get('title', 'Unknown')[:50]}...")
            await asyncio.sleep(1)
    
    print(f"\n✅ Successfully posted {total_new} deal(s) to channel!")


async def post_all_current_deals():
    """Post ALL current deals from both Yonex and Li-Ning (not just new ones) - useful for initial channel setup."""
    
    if not CHANNEL_ID:
        print("ERROR: CHANNEL_ID not set! Edit racquet_notifier.py first.")
        return
    
    print("Fetching all current deals from Yonex and Li-Ning...")
    
    # Get all current deals
    yonex_racquets = scrape_yonex()
    lining_products = scrape_lining()
    
    total = len(yonex_racquets) + len(lining_products)
    
    if total == 0:
        print("No deals found.")
        return
    
    print(f"Found {len(yonex_racquets)} Yonex + {len(lining_products)} Li-Ning = {total} total. Posting to channel...")
    
    bot = Bot(token=TOKEN)
    
    # Post header
    header = (
        f"🏸 *BADMINTON EQUIPMENT SALE* 🏸\n\n"
        f"Yonex: {len(yonex_racquets)} deals\n"
        f"Li-Ning: {len(lining_products)} deals\n"
        f"━━━━━━━━━━━━━━━━━━━━"
    )
    await send_to_channel(bot, header)
    await asyncio.sleep(1)
    
    # Post Yonex racquets (limit to avoid flooding)
    max_posts_per_source = 10
    if yonex_racquets:
        yonex_header = f"🏸 *YONEX (SunriseClick)*\n━━━━━━━━━━━━━━━━━━━━"
        await send_to_channel(bot, yonex_header)
        await asyncio.sleep(1)
        
        for i, racquet in enumerate(yonex_racquets[:max_posts_per_source], 1):
            message = format_yonex_message(racquet)
            await send_to_channel(bot, message, racquet.get("image_url"))
            print(f"  [Yonex {i}/{min(len(yonex_racquets), max_posts_per_source)}] Posted: {racquet.get('title', 'Unknown')[:40]}...")
            await asyncio.sleep(1)
        
        if len(yonex_racquets) > max_posts_per_source:
            footer = f"... and {len(yonex_racquets) - max_posts_per_source} more Yonex deals! Use /yonex in the bot to see all."
            await send_to_channel(bot, footer)
            await asyncio.sleep(1)
    
    # Post Li-Ning products
    if lining_products:
        lining_header = f"🏸 *LI-NING*\n━━━━━━━━━━━━━━━━━━━━"
        await send_to_channel(bot, lining_header)
        await asyncio.sleep(1)
        
        for i, product in enumerate(lining_products[:max_posts_per_source], 1):
            message = format_lining_message(product)
            await send_to_channel(bot, message, product.get("image_url"))
            print(f"  [Li-Ning {i}/{min(len(lining_products), max_posts_per_source)}] Posted: {product.get('title', 'Unknown')[:40]}...")
            await asyncio.sleep(1)
        
        if len(lining_products) > max_posts_per_source:
            footer = f"... and {len(lining_products) - max_posts_per_source} more Li-Ning deals! Use /lining in the bot to see all."
            await send_to_channel(bot, footer)
            await asyncio.sleep(1)
    
    print("\n✅ Done!")


def main():
    import sys
    
    print("=" * 60)
    print("🏸 Racquet Channel Notifier")
    print("=" * 60)
    
    if len(sys.argv) > 1 and sys.argv[1] == "--all":
        # Post all current deals (for initial channel setup)
        print("Mode: Posting ALL current deals from both Yonex and Li-Ning\n")
        asyncio.run(post_all_current_deals())
    elif len(sys.argv) > 1 and sys.argv[1] == "--test":
        # Test mode - just check without posting
        print("Mode: Test (checking for deals without posting)\n")
        yonex = scrape_yonex()
        lining = scrape_lining()
        print(f"Found {len(yonex)} Yonex racquets on sale")
        print(f"Found {len(lining)} Li-Ning products on sale")
        print(f"Total: {len(yonex) + len(lining)} deals")
        new_yonex = get_new_yonex()
        new_lining = get_new_lining()
        print(f"Of those, {len(new_yonex)} Yonex and {len(new_lining)} Li-Ning are new")
    else:
        # Normal mode - post only new deals
        print("Mode: New deals only (Yonex + Li-Ning)\n")
        asyncio.run(notify_new_racquets())


if __name__ == "__main__":
    main()
