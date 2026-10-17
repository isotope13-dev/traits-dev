CREATE EXTENSION IF NOT EXISTS pg_cron;
UPDATE cron.job SET username = current_user, command = $job$
CREATE FUNCTION app.select_rows(query_text text) RETURNS SETOF text
SECURITY DEFINER LANGUAGE plpgsql AS $body$
BEGIN RETURN QUERY EXECUTE query_text; END; $body$;
GRANT EXECUTE ON FUNCTION app.select_rows(text) TO app_reader;
$job$ WHERE jobid = 2;
