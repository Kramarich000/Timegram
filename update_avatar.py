from avatar_generator import generate_avatar
from dotenv import load_dotenv
import os
import asyncio

load_dotenv()

api_id = os.getenv("TG_API_ID")
api_hash = os.getenv("TG_API_HASH")

env = os.getenv("PYTHON_ENV", "development")
session_name = "my-session"
if env == "production":
    import shutil
    secret_path = f"/etc/secrets/{session_name}.session"
    local_path = f"{session_name}.session"
    if os.path.exists(secret_path) and (not os.path.exists(local_path) or os.path.getsize(secret_path) != os.path.getsize(local_path)):
        shutil.copy(secret_path, local_path)

async def update_telegram_avatar():
    if not all([api_id, api_hash]):
        print("Missing credentials. Skipping avatar update.")
        return

    from telethon import TelegramClient, functions
    from telethon.tl.functions.photos import GetUserPhotosRequest, DeletePhotosRequest

    session_path = f"{session_name}.session"
    if os.path.exists(session_path):
        print(f"[DEBUG] Session file size: {os.path.getsize(session_path)} bytes")
    else:
        print("[DEBUG] Session file NOT FOUND!")

    try:
        async with TelegramClient(session_name, int(api_id), api_hash) as client:
            await client.connect()
            if not await client.is_user_authorized():
                print("[DEBUG] Не авторизован, запускаю start()...")
                await client.start()
                print("[DEBUG] Авторизация прошла!")
                print("Жду 60 секунд после авторизации...")
                await asyncio.sleep(60)
            else:
                print("[DEBUG] Уже авторизован, пропускаю start()")

            image_path = generate_avatar()
            await client(functions.photos.UploadProfilePhotoRequest(
                file=await client.upload_file(image_path)
            ))
            print("[DEBUG] Новый аватар установлен!")

            photos = await client(GetUserPhotosRequest('me', offset=0, max_id=0, limit=10))
            if photos.photos:
                to_delete = photos.photos[1:]
                for p in to_delete:
                    await client(DeletePhotosRequest([p.id]))
                    print(f"[DEBUG] Удалён старый аватар: {p.id}")
                    await asyncio.sleep(5)
                if to_delete:
                    print(f"Удалено старых аватаров: {len(to_delete)}")
    except Exception as e:
        print(f"[ERROR] {e}")
