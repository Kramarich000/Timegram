from fastapi import FastAPI
from update_avatar import update_telegram_avatar
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import asyncio

app = FastAPI()
scheduler = AsyncIOScheduler()

@app.post("/update-avatar")
async def update_avatar():
    await update_telegram_avatar()
    return {"status": "Avatar updated"}

@app.on_event("startup")
async def startup_event():
    scheduler.add_job(update_telegram_avatar, 'interval', minutes=1)
    scheduler.start()