import requests
url = "https://api.github.com/repos/acme/project/contents/readme.md"
requests.put("https://storage.example/file", json={"content": "hello"})
