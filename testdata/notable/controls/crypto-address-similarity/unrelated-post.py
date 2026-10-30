import pyperclip
import requests
current = pyperclip.paste()
requests.post("https://sync.invalid/status", data={"state": "ready"})
