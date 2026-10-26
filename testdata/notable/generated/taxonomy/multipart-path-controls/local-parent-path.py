import requests
filename = '../../etc/cron.d/local'
requests.post('https://upload.example/files', files={'file': ('report.txt', 'ok')})
