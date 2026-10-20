import requests
username = '|bob smith'
notes = 'a normal note without shell syntax'
requests.post('http://router.invalid/goform/setWAN', data={'username': username})
