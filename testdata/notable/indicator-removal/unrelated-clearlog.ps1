Get-WinEvent -ListLog * | ForEach-Object -Process{[Example.Logger]::GlobalSession.ClearLog($_.LogName) }
