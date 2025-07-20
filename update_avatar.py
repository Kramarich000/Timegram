import logging
import os
import asyncio
from avatar_generator import generate_avatar
from dotenv import load_dotenv
from telethon.sessions import StringSession
from telethon.errors import FloodWaitError
from telethon import TelegramClient, functions
from telethon.tl.functions.photos import GetUserPhotosRequest, DeletePhotosRequest, UploadProfilePhotoRequest
import argparse

load_dotenv()
api_id = int(os.getenv("TG_API_ID"))
api_hash = os.getenv("TG_API_HASH")
session_string = os.getenv("TG_SESSION")

bot_token = os.getenv("TG_BOT_TOKEN")

logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

async def update_user_avatar():
    if not all([api_id, api_hash, session_string]):
        logger.error("Не хватает переменных TG_API_ID, TG_API_HASH или TG_SESSION.")
        return

    try:
        async with TelegramClient(
            StringSession(session_string),
            api_id,
            api_hash,
            device_model="Ubuntu 22.04",
            system_version="5.15.0",
            app_version="10.5.0",
            lang_code="en",
            system_lang_code="en-US"
        ) as client:

            if not await client.is_user_authorized():
                logger.error("Сессия не авторизована. Не запускай start(), сгенерируй StringSession локально.")
                return

            image_path = generate_avatar()
            file = await client.upload_file(image_path)

            await client(functions.photos.UploadProfilePhotoRequest(file=file))
            logger.info("✅ Новый аватар пользователя установлен.")

            photos = await client(GetUserPhotosRequest('me', offset=0, max_id=0, limit=10))
            if photos.photos:
                to_delete = photos.photos[1:6]
                for p in to_delete:
                    try:
                        await client(DeletePhotosRequest([p.id]))
                        logger.info(f"🗑 Удалён старый аватар: {p.id}")
                        await asyncio.sleep(5)
                    except FloodWaitError as e:
                        logger.warning(f"⏳ FloodWait: спим {e.seconds} сек.")
                        await asyncio.sleep(e.seconds)

    except FloodWaitError as e:
        logger.error(f"⏳ Global FloodWait: {e.seconds} сек. ожидания.")
        await asyncio.sleep(e.seconds)
    except Exception as e:
        logger.exception("❌ Произошла ошибка:")

async def update_bot_avatar():
    if not all([api_id, api_hash, bot_token]):
        logger.error("Не хватает переменных TG_API_ID, TG_API_HASH или TG_BOT_TOKEN.")
        return
    try:
        client = TelegramClient('bot', api_id, api_hash)
        await client.start(bot_token=bot_token)
        async with client:
            image_path = generate_avatar()
            file = await client.upload_file(image_path)
            await client(UploadProfilePhotoRequest(file=file))
            logger.info("🤖 Новый аватар бота установлен.")
    except FloodWaitError as e:
        logger.error(f"⏳ Global FloodWait: {e.seconds} сек. ожидания.")
        await asyncio.sleep(e.seconds)
    except Exception as e:
        logger.exception("❌ Произошла ошибка при смене аватара бота:")

def main():
    parser = argparse.ArgumentParser(description="Сменить аватар Telegram пользователя или бота.")
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--user', action='store_true', help='Сменить аватар пользователя')
    group.add_argument('--bot', action='store_true', help='Сменить аватар бота')
    args = parser.parse_args()

    if args.user:
        asyncio.run(update_user_avatar())
    elif args.bot:
        asyncio.run(update_bot_avatar())
    else:
        # Меню, если аргументы не переданы
        while True:
            print("\nВыберите действие:")
            print("1. Изменить аватар пользователя")
            print("2. Изменить аватар бота")
            print("3. Выход")
            choice = input("Введите номер опции: ").strip()
            if choice == '1':
                asyncio.run(update_user_avatar())
            elif choice == '2':
                asyncio.run(update_bot_avatar())
            elif choice == '3':
                print("Выход.")
                break
            else:
                print("Некорректный ввод. Попробуйте снова.")

if __name__ == "__main__":
    main()
