from requests import post
options = {"websiteURL": "https://site.example", "websiteKey": "public"}
post("https://queue.example/results", json=options)
