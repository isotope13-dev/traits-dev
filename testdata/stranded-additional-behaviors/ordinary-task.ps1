$Task = 'schtasks /Create /SC DAILY /TN Backup /TR backup.exe'
$Idle = 'schtasks /Create /SC ONIDLE /TN IdleBackup /TR backup.exe'
