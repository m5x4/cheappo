"""
Cheappo Telegram Bot
Main entry point for the bot
"""

from telegram.ext import Application, CommandHandler, MessageHandler, filters

from config import TOKEN
from commands import start_command, help_command, discounts_command, racquets_command, invalid_command
from handlers import handle_message, error_handler


def main():
    """Start the bot."""
    print('Starting bot...')
    
    # Create the Application
    app = Application.builder().token(TOKEN).build()
    
    # Register command handlers
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('nike', discounts_command))
    app.add_handler(CommandHandler('racquets', racquets_command))
    
    # Handle unknown commands (must be after valid commands)
    app.add_handler(MessageHandler(filters.COMMAND, invalid_command))
    
    # Register message handler for regular text
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Register error handler
    app.add_error_handler(error_handler)
    
    print('Bot is running! Press Ctrl+C to stop.')
    
    # Start polling (drop_pending_updates=True ignores messages sent while bot was offline)
    app.run_polling(poll_interval=3, drop_pending_updates=True)


if __name__ == '__main__':
    main()
