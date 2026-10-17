CREATE EXTENSION IF NOT EXISTS pg_cron;
SELECT cron.schedule('cleanup', '0 3 * * *', 'VACUUM');
UPDATE cron.job SET username = 'postgres', command = 'VACUUM' WHERE jobid = 2;
CREATE FUNCTION public.get_clock() RETURNS timestamptz
SECURITY DEFINER LANGUAGE sql AS 'SELECT current_timestamp';
GRANT EXECUTE ON FUNCTION public.get_clock() TO app_role;
ALTER SYSTEM SET archive_command = 'cp %p /backup/%f';
SELECT pg_reload_conf();
SELECT pg_switch_wal();
