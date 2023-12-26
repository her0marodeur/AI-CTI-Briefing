import os
from dotenv import load_dotenv
import requests

def send_telegram_message(message):
    # Load environment variables from .env file
    load_dotenv()

    # Retrieve the Telegram bot token from the environment variables
    telegram_bot_token = os.getenv("TELEGRAM_BOT_TOKEN")

    chat_id = os.getenv("TELEGRAM_CHAT_ID")

    params = {"chat_id":chat_id, "text":message}
    url = f"https://api.telegram.org/bot{telegram_bot_token}/sendMessage"
    requests.post(url, params=params)

    
