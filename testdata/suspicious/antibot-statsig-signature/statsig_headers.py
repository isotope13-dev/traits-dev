import time
import requests


def build_headers(token: str) -> dict:
    # Sends the request signature a web app checks against bots.
    return {
        "x-statsig-id": f"{int(time.time())}:{token}",
        "authorization": f"Bearer {token}",
    }


def fetch(url: str, token: str) -> requests.Response:
    return requests.get(url, headers=build_headers(token), timeout=10)
