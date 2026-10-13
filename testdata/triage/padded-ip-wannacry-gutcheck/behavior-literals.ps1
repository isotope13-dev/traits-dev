$user = '!admin'
$cookie = 'sid=x; Domain=example.com; HttpOnly'
$command = 'rundll32.exe x.dll,Entry'
$ua = 'User-Agent: diagnostic'
$transport = 'WinHttp.WinHttpRequest.5.1'
ipconfig /all
$x = 'HKCU:'
Get-ItemProperty -Path HKCU:\Software\Example
$events | Sort-Object TimeCreated | Select-Object -First 10
$x = 'CurrentVerticalResolution'
$protected = ConvertTo-SecureString -String $secret -AsPlainText -Force | ConvertFrom-SecureString
