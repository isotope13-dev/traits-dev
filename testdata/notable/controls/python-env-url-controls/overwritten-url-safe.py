import os
import requests

u = "https://collector.invalid/" + os.environ["AWS_SECRET_ACCESS_KEY"]
u = "https://service.invalid/safe"
requests.get(u)
