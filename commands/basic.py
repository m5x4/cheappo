"""
Basic Bot Commands
/start, /help
"""

from telegram import Update
from telegram.ext import ContextTypes
from config import BOT_USERNAME


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles the /start command"""
    welcome_text = (
        f"👋 Hello! I am *{BOT_USERNAME}*\n\n"
        "I help you find the best deals on:\n"
        "🏸 Badminton racquets\n"
        "👟 Nike products\n\n"
        "Use /help to see all commands!"
    )
    await update.message.reply_text(welcome_text, parse_mode="Markdown")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles the /help command"""
    help_text = (
        "🤖 *Available Commands:*\n\n"
        "/start - Start the bot\n"
        "/help - Show this help message\n"
        "/nike - Get Nike deals\n"
        "/racquets - Get badminton racquet deals (≥10% off)"
    )
    await update.message.reply_text(help_text, parse_mode="Markdown")

async def invalid_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles invalid commands"""
    await update.message.reply_text("❌ Invalid command. Use /help to see available commands.")