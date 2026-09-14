def operate():
    import os
    import requests
    output = os.environ.get("OUT_DIR", "")
    print(output)
    requests.post("https://collector.example.invalid/submit", data="build_started")

if False:
    operate()
