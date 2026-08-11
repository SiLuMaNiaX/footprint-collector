from fastapi import FastAPI, Request, HTTPException, Header
from datetime import datetime
import json
import os
import csv
from io import StringIO

app = FastAPI()

# Simple protection (change this token)
SECRET = "your_secret_token_here"

DATA_FILE = "/data/features.jsonl"
CSV_FILE = "/data/features.csv"

os.makedirs("/data", exist_ok=True)

@app.post("/webhook")
async def webhook(request: Request, authorization: str = Header(None)):
    # Optional simple protection
    # if authorization != f"Bearer {SECRET}":
    #     raise HTTPException(status_code=401, detail="Unauthorized")

    data = await request.json()
    data["received_at"] = datetime.utcnow().isoformat()

    # Save as JSONL
    with open(DATA_FILE, "a") as f:
        f.write(json.dumps(data) + "\n")

    return {"status": "ok"}

@app.get("/")
def home():
    return {"message": "Footprint Collector V2 is running"}

@app.get("/stats")
def stats():
    if not os.path.exists(DATA_FILE):
        return {"count": 0}

    with open(DATA_FILE, "r") as f:
        count = sum(1 for _ in f)

    return {"count": count, "file": DATA_FILE}

@app.get("/download")
def download():
    """Download all collected data as CSV"""
    if not os.path.exists(DATA_FILE):
        return {"error": "No data yet"}

    rows = []
    with open(DATA_FILE, "r") as f:
        for line in f:
            rows.append(json.loads(line))

    if not rows:
        return {"error": "Empty"}

    # Convert to CSV
    output = StringIO()
    writer = csv.DictWriter(output, fieldnames=rows[0].keys())
    writer.writeheader()
    writer.writerows(rows)

    from fastapi.responses import Response
    return Response(
        content=output.getvalue(),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=footprint_data.csv"}
    )
