# Syntax fixture only; never execute it.
def run(data):
    host = PowerShell.Create()
    host.AddScript(data)
    result = host.Invoke()
    return result
