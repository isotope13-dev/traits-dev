"""Benign near miss: OAuth token refresh goes directly to Google."""

import json
import urllib.request

TOKEN_ENDPOINT = "https://oauth2.googleapis.com/token"

def refresh(refresh_token):
    data = json.dumps({"refresh_token": refresh_token}).encode()
    request = urllib.request.Request(TOKEN_ENDPOINT, data=data, method="POST")
    return urllib.request.urlopen(request)
