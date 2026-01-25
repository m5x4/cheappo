"""
Racquets Command
/racquets - Fetch badminton racquet deals from SunriseClick
"""

from telegram import Update
from telegram.ext import ContextTypes
from scrapers.sunriseclick import scrape_sale_racquets, format_racquet_message


async def racquets_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles /racquets command to fetch badminton racquet deals from SunriseClick"""
    
    await update.message.reply_text("🔍 Searching for badminton racquet deals...")
    
    try:
        racquets = scrape_sale_racquets()
        
        if not racquets:
            await update.message.reply_text("No racquets with ≥10% discount found at the moment.")
            return
        
        # Send summary first
        await update.message.reply_text(
            f"🏸 Found *{len(racquets)}* racquet variants with ≥10% discount!\n"
            f"Showing top 5 deals:",
            parse_mode="Markdown"
        )
        
        # Send top 5 racquets
        for racquet in racquets[:5]:
            message = format_racquet_message(racquet)
            await update.message.reply_text(message, parse_mode="Markdown")
            
    except Exception as e:
        await update.message.reply_text(f"Error fetching racquets: {str(e)}")
