import requests
label = b'\x99\x85\x81\x84\xa8'.decode("cp1026")
requests.get("https://api.example.com/status")
