import os
import requests
def identity(value):
    return value
def run():
    identity(os.getenv("DEPLOY_API_KEY"))
    requests.post("https://collector.invalid", identity("status"))
