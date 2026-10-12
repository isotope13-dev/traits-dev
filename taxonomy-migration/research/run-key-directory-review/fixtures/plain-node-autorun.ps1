$script = Join-Path $env:APPDATA 'tray.js'
"console.log('Tray app started');" | Set-Content -Path $script
$run = 'HKCU:\Software\Microsoft\Windows\CurrentVersion\Run'
New-ItemProperty -Path $run -Name 'TrayApp' -Value ('node.exe "{0}"' -f $script) -PropertyType String -Force
