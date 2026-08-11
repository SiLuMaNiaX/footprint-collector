from fastapi import FastAPI, Request
from datetime import datetime
import json
import os
import uvicorn

app = FastAPI()

@app.post("/webhook")
async def receive_webhook(request: Request):
    data = await request.json()
    data["received_at"] = datetime.utcnow().isoformat()

    with open("features.jsonl", "a") as f:
        f.write(json.dumps(data) + "\n")

    return {"status": "ok"}

@app.get("/")
def home():
    return {"message": "Footprint collector is running"}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
