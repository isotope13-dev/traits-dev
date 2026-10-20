UPDATE cron.job SET username = 'postgres', command = $job$
DO $body$ BEGIN
CREATE FUNCTION restricted() RETURNS text SECURITY DEFINER
LANGUAGE sql AS 'SELECT current_user::text';
CREATE FUNCTION query_rows(sql text) RETURNS SETOF text
SECURITY INVOKER LANGUAGE plpgsql AS $fn$
BEGIN RETURN QUERY EXECUTE sql; END; $fn$;
GRANT EXECUTE ON FUNCTION query_rows(text) TO app_role;
END; $body$
$job$ WHERE jobid = 2;
