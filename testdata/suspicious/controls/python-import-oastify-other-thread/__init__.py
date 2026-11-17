import requests
from threading import Thread
def notify():
    try:
        requests.get('https://example.oastify.com/')
    except Exception:
        pass
Thread(target=other).start()
