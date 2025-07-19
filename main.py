from fastapi import FastAPI, Request, HTTPException
from update_avatar import update_telegram_avatar
from qstash_utils import verify_qstash_signature

app = FastAPI()

@app.post("/update-avatar")
async def update_avatar(request: Request):
    if not await verify_qstash_signature(request):
        raise HTTPException(status_code=403, detail="Invalid signature")

    await update_telegram_avatar()
    return {"status": "Avatar updated"}
