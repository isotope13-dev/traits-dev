# References and queries are capabilities, without theft or remote execution.
$database = 'C:\Windows\NTDS\ntds.dit'
Get-WmiObject -List Win32_Process -ComputerName $server
