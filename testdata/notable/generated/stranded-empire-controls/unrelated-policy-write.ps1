$PolicyNames = @('DisableCMD', 'DisableTaskMgr')
New-ItemProperty -Path 'HKCU:\Software\Example\Window' -Name 'Width' -Value 800
Write-Output $PolicyNames
