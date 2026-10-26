import base64
import google.auth

def authenticate(username, password):
    credentials, project = google.auth.default()
    data = f"{username}:{password}".encode()
    headers = {}
    headers["Authorization"] = f"Basic {base64.b64encode(data).decode()}"
    return headers, credentials, project
