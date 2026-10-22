"""Hand-written OWA session replay: a bearer body posted to the OWA token
endpoint with no detection-tool context. The bearer-body trait must fire
here (and the hostile replay composite with it)."""
import requests

token = refresh_access_token()
body = "token_type=Bearer&access_token=" + token
resp = requests.post(
    "https://outlook.office.com/owa/auth.owa",
    data=body,
    headers={"Content-Type": "application/x-www-form-urlencoded"},
)
resp.raise_for_status()
