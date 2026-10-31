# https://github.com/jennifer-language/jennifer
import requests
webhook_url = 'https://example.net/webhook/receive'
requests.post(webhook_url, json={'status': 'ok'})
