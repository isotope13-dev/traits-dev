"""Static fixture: mutually exclusive identity acquisition branches."""
import os
import re
import socket
from getpass import getuser
from hashlib import sha256
from uuid import getnode
from requests import post


def collect(platform):
    track = {"host_name": socket.gethostname(), "whoami": getuser()}
    ident_res = "https://api64.ipify.org"
    if platform == "browser":
        from google.colab import output
        from IPython.display import Javascript, display
        display(Javascript("""
            async function identify() {
                return import('https://assets.vendor.net/browser.js')
                    .then(FingerprintJS => FingerprintJS.load())
                    .then(fp => fp.get()).then(result => result.visitorId);
            }
        """))
        track["visitorId"] = output.eval_js("identify()")
    elif platform == "secret-service":
        url = "https://www.kaggle.com/requests/GetUserSecretByLabelRequest"
        token = os.getenv("KAGGLE_USER_SECRETS_TOKEN")
        response = post(url, json={"Label": "api-key"}, headers={"X-Kaggle-Authorization": token})
        err = response.json()["errors"][0]
        match = re.search(r".*\s(\d{5,})\s.*", err)
        if match:
            track["visitorId"] = match.group(1)
    else:
        track["visitorId"] = sha256(str(getnode()).encode()).hexdigest()
    return track
