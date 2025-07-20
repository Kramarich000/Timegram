from fastapi import FastAPI, Query
from contextlib import asynccontextmanager
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from update_avatar import update_user_avatar, update_bot_avatar
import asyncio

scheduler = AsyncIOScheduler()

def schedule_avatar_update(target: str):
    if target == "user":
        asyncio.create_task(update_user_avatar())
    elif target == "bot":
        asyncio.create_task(update_bot_avatar())

@asynccontextmanager
async def lifespan(app: FastAPI):
    # scheduler.add_job(lambda: schedule_avatar_update("user"), 'interval', minutes=5)
    # scheduler.add_job(lambda: schedule_avatar_update("bot"), 'interval', minutes=5)
    scheduler.start()
    yield
    scheduler.shutdown()

app = FastAPI(lifespan=lifespan)

@app.post("/update-avatar")
async def update_avatar(target: str = Query("bot", enum=["user", "bot"])):
    print(f"API вызван с target={target}")
    if target == "user":
        print("Вызов смены аватара пользователя")
        await update_user_avatar()
    elif target == "bot":
        print("Вызов смены аватара бота")
        await update_bot_avatar()
    return {"status": f"Avatar updated for {target}"}