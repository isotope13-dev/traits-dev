import os
import requests
from os.path import dirname
from dotenv import load_dotenv


def up(d):
    while d != dirname(d):
        if ".env" in os.listdir(d):
            return os.path.join(d, ".env")
        d = dirname(d)
    return None


def pull(target):
    for root, dirs, files in os.walk("."):
        if ".env" in files:
            load_dotenv(os.path.join(root, ".env"))
            break
    load_dotenv(up(os.path.abspath(".")))
    return requests.get(target, headers={"Cookie": f"session={os.getenv('SC')}"}).text
