import requests
requests.post("https://example.test/query", json={"type": "SELECT SLEEP(4)"})
