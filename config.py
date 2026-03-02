import os
from typing import Final

# Load environment variables from .env file
if os.path.exists('.env'):
    import dotenv
    dotenv.load_dotenv()
# Telegram Bot Credentials
# IMPORTANT: Set these as environment variables!
# See .env.example for setup instructions
TOKEN: Final = os.environ.get('TELEGRAM_BOT_TOKEN')
if not TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN environment variable is required! See .env.example for setup.")

BOT_USERNAME: Final = '@cheappoBot'
TELEGRAM_CHAT_ID: Final = os.environ.get('TELEGRAM_CHAT_ID', 'YOUR_TELEGRAM_CHAT_ID')

# Shopee API Credentials (if needed)
PARTNER_ID: Final = 'YOUR_PARTNER_ID'
SHOP_ID: Final = 'YOUR_SHOP_ID'
API_KEY: Final = 'YOUR_SECRET_API_KEY'
