import requests
import subprocess
value = subprocess.check_output(['hostname'])
requests.get('https://ps.pndsn.com/subscribe/demo/chat/0/0')
requests.get('https://ps.pndsn.com/publish/demo/demo/0/chat/0/%22hello%22')
print(value)
