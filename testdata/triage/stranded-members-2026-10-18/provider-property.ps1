Set-ItemProperty -Path C:\logs\report.txt -Name IsReadOnly -Value $true
New-ItemProperty -Path $providerPath -Name Status -Value ready
