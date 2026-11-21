$action = New-ScheduledTaskAction -Execute "conhost.exe" -Argument "--headless powershell.exe -EncodedCommand ZQB4AGkAdAA="
Register-ScheduledTask -TaskName "Maintenance" -Action $action
