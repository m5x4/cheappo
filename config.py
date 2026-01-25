import os
from typing import Final

# Telegram Bot Credentials
# Uses environment variable if set (for GitHub Actions), otherwise uses hardcoded value
TOKEN: Final = os.environ.get('TELEGRAM_BOT_TOKEN', '7933198908:AAGeEBuZ2-eNtEzeJOZatnuN0-b9J_vLXb0')
BOT_USERNAME: Final = '@cheappoBot'
TELEGRAM_CHAT_ID: Final = 'YOUR_TELEGRAM_CHAT_ID'

# Shopee API Credentials (if needed)
PARTNER_ID: Final = 'YOUR_PARTNER_ID'
SHOP_ID: Final = 'YOUR_SHOP_ID'
API_KEY: Final = 'YOUR_SECRET_API_KEY'
