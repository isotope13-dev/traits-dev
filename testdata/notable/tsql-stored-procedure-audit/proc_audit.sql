SET QUOTED_IDENTIFIER OFF
GO
SET ANSI_NULLS OFF
GO
DECLARE @db varchar(128), @name varchar(128)
DECLARE CursorDB CURSOR FOR
SELECT name FROM master..SYSDATABASES WHERE sid <> 1
OPEN CursorDB
FETCH NEXT FROM CursorDB INTO @db
WHILE @@FETCH_STATUS = 0
BEGIN
    SELECT o.name, c.text FROM sysobjects o INNER JOIN syscomments c ON c.id = o.id WHERE o.type = 'P'
    FETCH NEXT FROM CursorDB INTO @db
END
CLOSE CursorDB
DEALLOCATE CursorDB
GO
-- Example usage: ALTER PROCEDURE dbo.usp_Refresh AS SELECT 1
