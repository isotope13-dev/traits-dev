import os
import requests

environment = os.environ
requests.post("https://service.example/", json={"language": environment.get("LANG")})
