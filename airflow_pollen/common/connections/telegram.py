import os
import requests
from types import SimpleNamespace

from dotenv import load_dotenv


def Telegram():
    load_dotenv()
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")

    if not bot_token or not chat_id:
        raise ValueError(
            "TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID must be set in your .env file"
        )

    def send_message(text: str):
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        payload = {"chat_id": chat_id, "text": text}
        r = requests.post(url, data=payload)
        r.raise_for_status()
        return r.json()

    # this lets our function be called as
    # telegram_resource.send_message, and it also works for
    # using several functions in the future without need for
    # a class
    return SimpleNamespace(send_message=send_message)


telegram = Telegram()
