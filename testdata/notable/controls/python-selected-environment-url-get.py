import os
import requests

requests.get("https://service.example/" + os.environ.get("LANG", "en"))
