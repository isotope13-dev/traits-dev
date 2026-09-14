def operate():
    import os
    import requests
    token = os.environ.get("API_TOKEN", "")
    requests.get("https://service.example.invalid/status", headers={"Authorization": "Bearer " + token})
