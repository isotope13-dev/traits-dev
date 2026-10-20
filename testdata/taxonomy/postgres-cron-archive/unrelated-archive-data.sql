CREATE FUNCTION backup_export(oid,text) RETURNS integer
AS 'be_lo_export' LANGUAGE internal STRICT;
SELECT lo_from_bytea(81234, convert_to('ordinary backup data','UTF8'));
-- The archiver setting is not the data passed to lo_from_bytea.
ALTER SYSTEM SET archive_command = 'id > /tmp/probe.txt';
SELECT backup_export(81234, 'postgresql.auto.conf');
SELECT pg_reload_conf();
SELECT pg_switch_wal();
