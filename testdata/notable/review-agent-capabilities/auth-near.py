import os, json, urllib.request
ai = os.getenv("OPENAI_API_KEY")
aws = os.getenv("AWS_SECRET_ACCESS_KEY")
body = json.dumps({"query": "status"}).encode()
req = urllib.request.Request("https://api.example/query", data=body, headers={"Authorization": "Bearer " + ai})
urllib.request.urlopen(req)
