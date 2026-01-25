import requests
from config import TOKEN, TELEGRAM_CHAT_ID

def send_to_telegram(message):
    """Sends a message to the Telegram bot"""
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {"chat_id": TELEGRAM_CHAT_ID, "text": message, "parse_mode": "Markdown"}
    requests.post(url, data=data)
