import os
import requests


def fetch_tree(endpoint_path):
    url = "https://api.github.com/repos/example/project/" + endpoint_path
    token = os.environ.get("GITHUB_TOKEN")
    headers = {"Authorization": "token {}".format(token)} if token else {}
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    return resp.json()
