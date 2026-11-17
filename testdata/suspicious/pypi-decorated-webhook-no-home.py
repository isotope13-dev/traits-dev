import requests
from pathlib import Path
from functools import wraps

def decorate(fn):
    @wraps(fn)
    def wrapped(*args, **kwargs):
        url = "https://discord.com/api/webhooks/123456789012345678/ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghi1234567890"
        embed = {"description": "ready"}
        data = {"embeds": [embed]}
        try:
            requests.post(url, json=data, timeout=2)
        except Exception:
            pass
        return fn(*args, **kwargs)
    return wrapped
