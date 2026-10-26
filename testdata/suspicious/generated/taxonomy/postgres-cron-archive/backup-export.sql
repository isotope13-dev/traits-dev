CREATE FUNCTION dump_object(oid, text) RETURNS integer
AS 'lo_export' LANGUAGE 'internal' STRICT;
SELECT lo_from_bytea(98231, convert_to($cfg$archive_command = 'cp %p /backup/%f'
$cfg$, 'UTF8'));
SELECT dump_object(98231, 'postgresql.auto.conf');
SELECT pg_reload_conf();
SELECT pg_switch_wal();
