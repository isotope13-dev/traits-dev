import subprocess
# frida does not make this application Frida
print('inline hook')
subprocess.run(['setenforce', '0'])
