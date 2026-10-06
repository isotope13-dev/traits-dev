"""Benign control: small self-hosted Ollama fleet client.

Two operator-owned servers, one health check each, no worker pool, no
search-engine discovery, no endpoint swarm. Must stay below every
hostile/suspicious threshold.
"""
import requests

_OWN_SERVERS = [
    "http://10.0.0.11:11434",
    "http://10.0.0.12:11434",
]


def check_server(url):
    resp = requests.get(f"{url}/api/tags", timeout=5)
    return [m.get("name", "") for m in resp.json().get("models", [])]


def list_models():
    inventory = {}
    for url in _OWN_SERVERS:
        inventory[url] = check_server(url)
    return inventory
