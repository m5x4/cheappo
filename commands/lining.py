"""
Li-Ning Products Telegram Bot Command
"""

from telegram import Update
from telegram.ext import ContextTypes
from scrapers.lining import scrape_sale_products, format_product_message


async def lining_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handle /lining command - show Li-Ning products on sale with >=10% discount
    """
    await update.message.reply_text("🏸 Fetching Li-Ning badminton products on sale... Please wait...")
    
    try:
        # Scrape current sale products
        products = scrape_sale_products()
        
        if not products:
            await update.message.reply_text(
                "❌ No Li-Ning products found with ≥20% discount and ≥$50 original price right now."
            )
            return
        
        # Send header message
        await update.message.reply_text(
            f"🏸 *Li-Ning Sale Products*\n\n"
            f"Found *{len(products)}* products with ≥20% discount!\n"
            f"(Min original price: $50)\n\n"
            f"Sending top deals...",
            parse_mode="Markdown"
        )
        
        # Send each product (limit to top 20 to avoid spam)
        for product in products[:20]:
            message = format_product_message(product)
            
            # Send with photo if available
            if product.get("image_url"):
                try:
                    await update.message.reply_photo(
                        photo=product["image_url"],
                        caption=message,
                        parse_mode="Markdown"
                    )
                except Exception as e:
                    # Fallback to text if image fails
                    await update.message.reply_text(message, parse_mode="Markdown")
            else:
                await update.message.reply_text(message, parse_mode="Markdown")
        
        # If there are more products, send summary
        if len(products) > 20:
            await update.message.reply_text(
                f"📊 *Summary*\n\n"
                f"Showing top 20 out of {len(products)} total products.\n"
                f"Visit Li-Ning website for more deals!",
                parse_mode="Markdown"
            )
    
    except Exception as e:
        print(f"Error in lining command: {e}")
        await update.message.reply_text(
            "❌ Error fetching Li-Ning products. Please try again later."
        )
