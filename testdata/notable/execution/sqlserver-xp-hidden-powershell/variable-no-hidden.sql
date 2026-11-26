DECLARE @cmd NVARCHAR(4000) = N'bcp db.dbo.t out D:\o.csv -c -T';
EXEC master..xp_cmdshell @cmd;
