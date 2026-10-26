$Task = 'schtasks /Create /SC DAILYREPORT /TN Backup /TR backup.exe'
$Idle = 'schtasks /Create /SC ONIDLER /TN IdleBackup /TR backup.exe'
