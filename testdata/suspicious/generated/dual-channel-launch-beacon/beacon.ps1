$exe=Join-Path $env:USERPROFILE 'Downloads\Install42.exe'
Start-Process -FilePath $exe
$w=[Net.HttpWebRequest]::Create('https://updates.vendor-ops.net/api?event=launch_ok')
$w.Method='GET'
$r=$w.GetResponse()
$r.Close()
Start-Process -FilePath curl.exe -WindowStyle Hidden -ArgumentList @('-s','-o','NUL','https://updates.vendor-ops.net/api?event=launch_ok')
