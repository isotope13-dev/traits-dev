"""Telegram echo bot: replies to each message with its upper-cased text."""
import json
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


def serve(token, chat):
    offset = 0
    while True:
        data = _api(token, "getUpdates", {"offset": offset, "timeout": 20})
        for update in data.get("result", []):
            offset = update["update_id"] + 1
            msg = update.get("message") or {}
            text = msg.get("text") or ""
            _api(token, "sendMessage", {"chat_id": chat, "text": text.upper()})
