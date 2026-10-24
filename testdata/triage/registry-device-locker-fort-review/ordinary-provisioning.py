import requests
session = requests.Session()
endpoint = "https://device.invalid/api/v2.0/cmdb/system/admin"
data = {"access-profile": "prof_admin", "trusthostv4": "10.0.0.0/24", "password": "operator-supplied"}
session.post(endpoint, json=data, verify=True)
