import requests
while True:
    try:
        source = requests.get("https://updates.example.net/stage").text
        print(source)
    except Exception:
        pass
