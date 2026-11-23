import os
import requests
requests.post("https://example.invalid/api", headers={"Authorization": os.environ["API_KEY"]}, data={"message": "hello"})
