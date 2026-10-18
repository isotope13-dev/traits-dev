$osv = (Get-WmiObject Win32_OperatingSystem).Version
$endpoint = "http://93.184.216.34:8080/health"
schtasks /create /tn "HealthCheck" /tr "powershell -file C:\Tools\health.ps1" /sc minute /mo 5 /ru SYSTEM /f
