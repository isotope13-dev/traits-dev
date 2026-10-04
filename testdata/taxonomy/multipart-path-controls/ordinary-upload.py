import requests
payload = '* * * * * root /bin/true\n'
requests.post('https://upload.example/files', files={'file': ('report.txt', payload)})
