def run(data):
    host = PowerShell.Create()
    host.AddScript(data)
    result = host.BeginInvoke(buffer, buffer)
    return result
