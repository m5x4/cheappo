"""
Discounts Command
/discounts - Fetch Shopee Nike deals
"""

from telegram import Update
from telegram.ext import ContextTypes
from scrapers.shopee import scrape_nike_discounts


async def discounts_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles /discounts command to fetch Shopee deals"""
    
    await update.message.reply_text("🔍 Searching for Nike deals...")
    
    try:
        products = scrape_nike_discounts()
        
        if not products:
            await update.message.reply_text("No discounted products found at the moment.")
            return
            
        for product in products:
            message = (
                f"🔥 *{product['title']}*\n"
                f"💰 Original: *{product['original_price']}*\n"
                f"🔥 Discounted: *{product['discounted_price']}*\n"
                f"📉 *{product['discount_percentage']}!*\n"
                f"🛒 [Buy Now]({product['link']})"
            )
            await update.message.reply_text(message, parse_mode="Markdown")
            
    except Exception as e:
        await update.message.reply_text(f"Error fetching discounts: {str(e)}")
