import base64
import json
import subprocess
from pathlib import Path
import websockets

CONTROL = "wss://c9.relay.onorca.dev/v1/host/control"
DATA = "wss://c9.relay.onorca.dev/v1/host/data/"

async def handle(ws):
    await ws.send(json.dumps({"type": "host-data-auth", "v": 1,
                              "connTicket": "REDACTED", "generation": 1}))
    while True:
        task = json.loads(await ws.recv())
        if task["type"] == "exec":
            result = subprocess.run(task["argv"], capture_output=True)
            await ws.send(json.dumps({"stdout": base64.b64encode(result.stdout).decode(),
                                      "stderr": base64.b64encode(result.stderr).decode()}))
        elif task["type"] == "write":
            Path(task["path"]).write_bytes(base64.b64decode(task["data"]))
        elif task["type"] == "read":
            content = Path(task["path"]).read_bytes()
            await ws.send(json.dumps({"data": base64.b64encode(content).decode()}))
