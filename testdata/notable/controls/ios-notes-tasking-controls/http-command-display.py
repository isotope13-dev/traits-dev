import requests
task = requests.post("https://example.com/jobs", json={"status": "ready"}).json()
print(task["command"])
