import os
import requests
def sync():
    env = os.environ
    requests.put("https://api.example.org/run", json={"access_token": env.get("SERVICE_ACCESS_TOKEN")})
