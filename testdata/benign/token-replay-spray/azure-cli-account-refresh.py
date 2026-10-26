"""Refresh the local user's cached Azure CLI accounts.

A developer CLI legitimately walks its own account cache and redeems each
account's refresh token as the Azure CLI first-party client.  It never
signs in as Office or the Authentication Broker.
"""
import requests

accounts = [
    {"tenant": "contoso.onmicrosoft.com", "refresh_token": "cached-a"},
    {"tenant": "fabrikam.onmicrosoft.com", "refresh_token": "cached-b"},
]
for account in accounts:
    response = requests.post(
        f"https://login.microsoftonline.com/{account['tenant']}/oauth2/v2.0/token",
        data={
            "grant_type": "refresh_token",
            "client_id": "04b07795-8ddb-461a-bbee-02f9e1bf7b46",
            "refresh_token": account["refresh_token"],
            "scope": "https://management.core.windows.net//.default",
        },
        timeout=20,
    )
    print(account["tenant"], response.status_code)
