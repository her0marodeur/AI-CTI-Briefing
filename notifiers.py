import os
from dotenv import load_dotenv
from telegram import Bot

def send_telegram_message(message):
    # Load environment variables from .env file
    load_dotenv()

    # Retrieve the Telegram bot token from the environment variables
    telegram_bot_token = os.getenv("TELEGRAM_BOT_TOKEN")

    chat_id = os.getenv("TELEGRAM_CHAT_ID")

    bot = Bot(token=telegram_bot_token)
    bot.send_message(chat_id=chat_id, text=message)


    
message = "Hello, this is a test message from my Telegram bot."
send_telegram_message(message)
