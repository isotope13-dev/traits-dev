"""A local check-in manager serving its own API: defining the route is the
other side of a beacon, not a phone-home path."""
from fastapi import FastAPI

app = FastAPI()


@app.post("/api/checkin")
async def batch_checkin():
    return {"ok": True, "results": []}


@app.get("/api/health")
async def health():
    return {"ok": True}
