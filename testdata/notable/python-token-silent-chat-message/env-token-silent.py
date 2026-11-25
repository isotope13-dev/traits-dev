import os, requests
TOKEN = os.environ["NOTIFY_TOKEN"]
CHAT = os.environ["NOTIFY_CHAT"]
def send(text):
    try:
        requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", data={"chat_id": CHAT, "text": text}, timeout=5)
    except Exception:
        pass
