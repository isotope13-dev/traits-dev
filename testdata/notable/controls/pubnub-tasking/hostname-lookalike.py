import requests
import subprocess
value = subprocess.check_output(['hostname'])
requests.get('https://ps.pndsn.com.example.invalid/subscribe/demo/chat/0/0')
requests.get('https://ps.pndsn.com.example.invalid/publish/demo/demo/0/chat/0/%22hello%22')
print(value)
