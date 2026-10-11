import requests
import pyperclip

def run():
    return requests.get("https://example.invalid/"), pyperclip.paste()
