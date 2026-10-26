"""Help-desk authenticator reset for one user who lost their phone.

Uses an administrator's own delegated token supplied by the environment;
it does not redeem anyone else's refresh token.
"""
import os

import requests

headers = {"Authorization": "Bearer " + os.environ["ADMIN_ACCESS_TOKEN"]}
user = os.environ["TARGET_USER_ID"]
old = requests.get(
    f"https://graph.microsoft.com/v1.0/users/{user}/authentication/phoneMethods",
    headers=headers, timeout=20,
).json()
for method in old.get("value", []):
    requests.delete(
        f"https://graph.microsoft.com/v1.0/users/{user}/authentication/phoneMethods/{method['id']}",
        headers=headers, timeout=20,
    )
requests.post(
    f"https://graph.microsoft.com/v1.0/users/{user}/authentication/microsoftAuthenticatorMethods",
    headers=headers,
    json={
        "@odata.type": "#microsoft.graph.microsoftAuthenticatorAuthenticationMethod",
        "displayName": "Replacement phone",
    },
    timeout=20,
)
