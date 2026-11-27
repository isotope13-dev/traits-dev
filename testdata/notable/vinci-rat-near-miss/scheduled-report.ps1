# Registers a nightly disk report task for the helpdesk.
$action = New-ScheduledTaskAction -Execute 'powershell.exe' -Argument '-NoProfile -File C:\Scripts\disk-report.ps1'
$trigger = New-ScheduledTaskTrigger -Once -At 2am -RepetitionInterval (New-TimeSpan -Hours 24)
Register-ScheduledTask -TaskName 'DiskReport' -Action $action -Trigger $trigger -User 'SYSTEM'
