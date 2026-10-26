def run(data):
    first = PowerShell.Create()
    second = PowerShell.Create()
    first.AddScript(data)
    result = second.Invoke()
    return result
