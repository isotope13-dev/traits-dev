Set s=CreateObject("WScript.Shell")
x="powershell -executionpolicy bypass -c $req=[System.Net.WebRequest]::Create('https://example.invalid/a');$res=$req.GetResponse();Write-Output $res.StatusCode"
s.Run(x),0,false
