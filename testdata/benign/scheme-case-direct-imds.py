import requests
token = requests.put("HTTP://169.254.169.254/latest/api/token/", headers={"X-aws-ec2-metadata-token-ttl-seconds": "21600"}).text
credentials = requests.get("HTTP://169.254.169.254/latest/meta-data/iam/security-credentials/node-role", headers={"X-aws-ec2-metadata-token": token})
