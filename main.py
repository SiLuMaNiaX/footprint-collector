from fastapi import FastAPI, Request
from datetime import datetime
import json
import os

app = FastAPI()

# Now writing to the persistent volume
DATA_FILE = "/data/features.jsonl"

@app.post("/webhook")
async def receive_webhook(request: Request):
    data = await request.json()
    data["received_at"] = datetime.utcnow().isoformat()

    # Create the file if it doesn't exist
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)

    with open(DATA_FILE, "a") as f:
        f.write(json.dumps(data) + "\n")

    print(f"Saved: {data.get('symbol')} | delta={data.get('delta')} | time={data.get('time')}")
    return {"status": "ok"}

@app.get("/")
def home():
    return {"message": "Footprint collector is running (persistent storage)"}

@app.get("/count")
def count_records():
    if not os.path.exists(DATA_FILE):
        return {"count": 0, "message": "No data yet"}

    with open(DATA_FILE, "r") as f:
        lines = f.readlines()

    last = json.loads(lines[-1]) if lines else None
    return {
        "count": len(lines),
        "last_record": last
    }
