import requests
r = requests.get('https://raw.githubusercontent.com/example/repo/main/config.txt')
print(r.text)
