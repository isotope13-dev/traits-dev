"""CI helper: log into the container registry API, then reuse the token."""

import json
import os

import requests


def login():
    """Exchange env-provided registry credentials for a bearer token."""
    username = os.environ.get("REGISTRY_USERNAME", "")
    password = os.environ["REGISTRY_PASSWORD"]
    response = requests.post(
        "https://registry.example.com/v2/users/login/",
        headers={"Content-Type": "application/json"},
        data=json.dumps({"username": username, "password": password}),
        timeout=30,
    )
    token = response.json()["token"]
    return {"Authorization": "Bearer " + token}


def delete_tag(image, tag):
    """Delete one image tag through the authenticated registry API."""
    headers = login()
    response = requests.delete(
        "https://registry.example.com/v2/repositories/" + image + "/tags/" + tag + "/",
        headers=headers,
        timeout=30,
    )
    response.raise_for_status()
