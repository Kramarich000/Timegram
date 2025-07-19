import os
from telethon.sync import TelegramClient
from dotenv import load_dotenv

load_dotenv()

api_id = os.getenv("TG_API_ID")
api_hash = os.getenv("TG_API_HASH")

if __name__ == "__main__":
    session_filename = "tg-session-file"
    with TelegramClient(session_filename, api_id, api_hash) as client:
        print("Сессия успешно создана!")