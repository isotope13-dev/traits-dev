import requests
repo = requests.get('https://api.github.com/user/repos').json()
metadata = {'private': False}
