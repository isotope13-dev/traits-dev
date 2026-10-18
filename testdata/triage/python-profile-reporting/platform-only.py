import json, platform, urllib.request
profile = {"platform": platform.system(), "node_id": "configured-id"}
request = urllib.request.Request("https://example.com/enroll", data=json.dumps(profile).encode(), method="POST")
urllib.request.urlopen(request)
