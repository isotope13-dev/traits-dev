param([string]$Command)
$enable = "sp_configure 'xp_cmdshell',1; RECONFIGURE"
$execute = "EXEC master..xp_cmdshell '$Command'"
