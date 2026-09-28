import requests
requests.put("https://api.github.com/repos/acme/project/contents/readme.md", json={"content": "hello"})
