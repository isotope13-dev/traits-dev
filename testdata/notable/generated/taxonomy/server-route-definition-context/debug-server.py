"""An application's own diagnostics endpoint: defining the route is not
phoning Shub telemetry home."""
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Events(BaseModel):
    events: list


@app.post("/api/debug/events")
def debug_events(req: Events):
    return {"ok": True, "recorded": len(req.events)}
