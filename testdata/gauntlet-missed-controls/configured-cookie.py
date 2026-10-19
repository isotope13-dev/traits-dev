import os
import requests
from dotenv import load_dotenv


def get_input(url):
    for root, dirs, files in os.walk('.'):
        if '.env' in files:
            load_dotenv(os.path.join(root, '.env'))
            break
    headers = {'Cookie': f"session={os.getenv('SESSION_COOKIE')}"}
    return requests.get(url, headers=headers).text
