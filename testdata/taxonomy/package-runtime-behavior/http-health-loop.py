import requests
import time
while not ready:
    response = requests.get(f"http://{host}:{port}/ping")
    ready = response.status_code == 200
    time.sleep(0.1)
