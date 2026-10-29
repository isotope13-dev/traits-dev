@echo off
goto :eof
$Scans = 'C:\ProgramData\Microsoft\Windows Defender\Scans'
$Service = "$Scans\History\Service"
$TA = New-ScheduledTaskAction -Execute 'cmd.exe' -Argument '/c echo health'
$TT = New-ScheduledTaskTrigger -AtStartup
$TP = New-ScheduledTaskPrincipal -UserId "SYSTEM" -LogonType ServiceAccount
Register-ScheduledTask -Force -Action $TA -Trigger $TT -Principal $TP -TaskName 'CheckHealth'
