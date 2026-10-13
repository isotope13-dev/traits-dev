import subprocess
import zipfile
from requests import post
subprocess.run(['schtasks.exe', '/delete', '/tn', 'Example'])
subprocess.run(['schtasks', '/create', '/tn', 'Example'])
subprocess.run(['schtasks', '/change', '/tn', 'Example'])
archive = zipfile.ZipFile('example.zip')
archive.extract('example.txt')
task_type = 'RecaptchaV2TaskProxyless'
post('https://solver.example/createTask', json={'type': task_type})
post('https://solver.example/getTaskResult', json={'taskId': 1})
command = 'pip install requests'
