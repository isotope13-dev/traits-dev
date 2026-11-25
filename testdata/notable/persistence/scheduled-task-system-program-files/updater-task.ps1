$taskAction = New-ScheduledTaskAction -Execute "C:\Program Files\Contoso\Updater\updater.exe" -Argument "/service"
$taskTrigger = New-ScheduledTaskTrigger -AtStartup
$taskPrincipal = New-ScheduledTaskPrincipal -UserId "SYSTEM" -RunLevel Highest -LogonType ServiceAccount
Register-ScheduledTask -TaskName "ContosoUpdater" -Action $taskAction -Trigger $taskTrigger -Principal $taskPrincipal -Force
