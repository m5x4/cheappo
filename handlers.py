"""
Message Handlers
Handles non-command messages and errors
"""

from telegram import Update
from telegram.ext import ContextTypes


def handle_response(text: str) -> str:
    """Process user text messages and return a response."""
    processed = text.lower()
    
    # Add custom responses here
    if 'hello' in processed or 'hi' in processed:
        return 'Hello! Use /help to see available commands.'
    
    return 'Please use any of the /commands!'


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles incoming text messages."""
    text = update.message.text
    user_id = update.message.chat.id
    
    print(f'User ({user_id}): {text}')
    
    response = handle_response(text)
    await update.message.reply_text(response)


async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles errors in the bot."""
    print(f'Update {update} caused error {context.error}')
