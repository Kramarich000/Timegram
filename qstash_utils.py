import os
import base64
import hmac
import hashlib
from fastapi import Request

current_key = os.getenv("QSTASH_CURRENT_SIGNING_KEY")
next_key = os.getenv("QSTASH_NEXT_SIGNING_KEY")

async def verify_qstash_signature(request: Request) -> bool:
    signature = request.headers.get("Upstash-Signature")
    if not signature:
        return False

    body = await request.body()
    url = str(request.url)

    def check(key):
        key_bytes = base64.b64decode(key)
        msg = url.encode() + b"\n" + body
        computed = hmac.new(key_bytes, msg, hashlib.sha256).digest()
        return hmac.compare_digest(base64.b64encode(computed).decode(), signature)

    return check(current_key) or (next_key and check(next_key))
