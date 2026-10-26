import requests
session = requests.Session()
for account, candidate in credential_pairs:
    response = session.post("https://device.invalid/logincheck", data={"username": saved_user, "secretkey": saved_password}, verify=True)
