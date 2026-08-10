from fastapi import FastAPI, Request, HTTPException, Header
from datetime import datetime
import json
import os

app = FastAPI()

# Simple security token (change this!)
SECRET_TOKEN = "my_secret_token_123"   # ← change this to something only you know

# File where we will store all features
DATA_FILE = "features.jsonl"

@app.post("/webhook")
async def receive_webhook(request: Request, authorization: str = Header(None)):
    # Security check
    if authorization != f"Bearer {SECRET_TOKEN}":
        raise HTTPException(status_code=401, detail="Unauthorized")

    data = await request.json()

    # Add server receive time
    data["received_at"] = datetime.utcnow().isoformat()

    # Append to file (one JSON per line)
    with open(DATA_FILE, "a") as f:
        f.write(json.dumps(data) + "\n")

    return {"status": "ok", "message": "Feature received"}

@app.get("/")
def health():
    return {"status": "running", "service": "Footprint Feature Collector"}