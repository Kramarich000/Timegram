from avatar_generator import generate_avatar
from dotenv import load_dotenv
import os

load_dotenv()

api_id = os.getenv("TG_API_ID")
api_hash = os.getenv("TG_API_HASH")
session_name = os.getenv("TG_SESSION_NAME")

async def update_telegram_avatar():
    if not api_id or not api_hash or not session_name:
        print("Telegram credentials are missing. Skipping avatar update.")
        return
    from telethon import TelegramClient, functions

    client = TelegramClient(session_name, int(api_id), api_hash)
    await client.start()
    image_path = generate_avatar()
    await client(functions.photos.UploadProfilePhotoRequest(
        file=await client.upload_file(image_path)
    ))
    await client.disconnect()
