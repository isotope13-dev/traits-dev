import requests
BOT_TOKEN = '123456789:ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghi'
url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'
requests.post(url, data={'chat_id': '42', 'text': 'Build completed'})
