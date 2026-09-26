"""Benign fixture: a self-hosted personal assistant with an opt-in bot.

The Telegram token lives in the local user's own profile and defaults to
empty; update polling starts only after the user configures it. Autostart
entries are managed by an explicit user-invoked add/remove tool.
"""
import queue
import subprocess
import urllib.request

PROFILE = {}
input_queue = queue.Queue()


def poll_telegram():
    token = PROFILE.get("tg_token", "")
    chat_id = PROFILE.get("tg_chat_id", "")
    if not token or not chat_id:
        return
    url = "https://api.telegram.org/bot%s/getUpdates?timeout=30" % token
    with urllib.request.urlopen(url, timeout=35) as resp:
        for text in resp.read().decode().splitlines():
            input_queue.put({"source": "telegram", "text": text})


def run_shell(command, timeout=60):
    return subprocess.run(
        command, shell=True, capture_output=True, text=True, timeout=timeout
    ).stdout


def autostart_manage(action, name, command):
    marker = "# startup_manage:%s" % name
    current = subprocess.run(
        ["crontab", "-l"], capture_output=True, text=True
    ).stdout
    if action == "add":
        entry = "@reboot %s %s\n" % (command, marker)
        subprocess.run(["crontab", "-"], input=current + entry, text=True)
        return "added"
    lines = [l for l in current.splitlines() if marker not in l]
    subprocess.run(["crontab", "-"], input="\n".join(lines), text=True)
    return "removed"
