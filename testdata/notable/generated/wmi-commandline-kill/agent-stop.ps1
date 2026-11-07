gcim Win32_Process | Where-Object { $_.CommandLine -match 'agent\.exe' } | ForEach-Object { Stop-Process -Id $_.ProcessId }
