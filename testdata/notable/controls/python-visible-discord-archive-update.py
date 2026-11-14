"""Near miss: visible updater downloads and opens a Discord-hosted archive."""

import subprocess
import requests


def stage_update():
    requests.get("https://pastebin.com/raw/release-notes")
    archive_url = "https://cdn.discordapp.com/attachments/123456789012345678/987654321098765432/update.zip"
    payload = requests.get(archive_url)
    destination = r"C:\Users\Public\Temp\update.zip"
    with open(destination, "wb") as output:
        output.write(payload.content)
    subprocess.Popen(["explorer.exe", destination])
