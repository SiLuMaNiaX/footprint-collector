from fastapi import FastAPI, Request
from datetime import datetime
import json
import os

app = FastAPI()

DATA_FILE = "features.jsonl"

@app.post("/webhook")
async def receive_webhook(request: Request):
    data = await request.json()
    data["received_at"] = datetime.utcnow().isoformat()

    with open(DATA_FILE, "a") as f:
        f.write(json.dumps(data) + "\n")

    print(f"Received data from {data.get('symbol')} at {data.get('time')}")  # shows in logs
    return {"status": "ok"}

@app.get("/")
def home():
    return {"message": "Footprint collector is running"}

@app.get("/count")
def count_records():
    if not os.path.exists(DATA_FILE):
        return {"count": 0, "message": "No data file yet"}
    
    with open(DATA_FILE, "r") as f:
        lines = f.readlines()
    
    return {
        "count": len(lines),
        "last_record": json.loads(lines[-1]) if lines else None
    }
