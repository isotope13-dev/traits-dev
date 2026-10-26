import os
import re
from requests import post


def identify_visitor():
    token = os.getenv("KAGGLE_USER_SECRETS_TOKEN")
    response = post("https://www.kaggle.com/requests/GetUserSecretByLabelRequest",
                    headers={"X-Kaggle-Authorization": f"Bearer {token}"},
                    json={"Label": "analytics-id"})
    err = response.json()["errors"][0]
    match = re.search(r".*\s(\d{5,})\s.*", err)
    track = {}
    if match:
        track["visitorId"] = match.group(1)
    return track
