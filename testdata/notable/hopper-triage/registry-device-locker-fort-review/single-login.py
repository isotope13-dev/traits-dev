import requests
session = requests.Session()
username, password = "admin", "operator-supplied"
resp = session.post("https://device.invalid/logincheck", data={"username": username, "secretkey": password}, verify=False)
