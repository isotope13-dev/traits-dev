import requests
requests.post("https://site.example/wp-json/batch/v1", json={
    "requests": [
        {"path": "http://", "body": {"route": "/wp/v2/posts"}},
        {"path": "https://:", "body": {"route": "/wp/v2/widgets"}},
    ]
})
