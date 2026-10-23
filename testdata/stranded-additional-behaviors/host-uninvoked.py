def run(data):
    host = PowerShell.Create()
    host.AddScript(data)
    return host
