import os
import requests
from dotenv import load_dotenv


def locate():
    cur_dir = os.path.abspath(".")
    while True:
        if ".env" in os.listdir(cur_dir):
            return os.path.join(cur_dir, ".env")
        up_dir = os.path.dirname(cur_dir)
        if up_dir == cur_dir:
            break
        cur_dir = up_dir


def fetch(url):
    for root, dirs, files in os.walk("."):
        if ".env" in files:
            load_dotenv(os.path.join(root, ".env"))
            break
    load_dotenv(locate())
    headers = {"Cookie": f"session={os.getenv('TOKEN')}"}
    return requests.get(url, headers=headers).text
