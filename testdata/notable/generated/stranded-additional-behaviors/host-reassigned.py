def run(data):
    host = PowerShell.Create()
    host.AddScript(data)
    host = unrelated_host()
    result = host.Invoke()
    return result
