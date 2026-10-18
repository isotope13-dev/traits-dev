import psycopg
with psycopg.connect("postgresql://localhost/postgres") as conn:
    conn.execute("CREATE FUNCTION allowed() RETURNS text SECURITY DEFINER LANGUAGE sql AS 'SELECT current_user::text';")
    conn.execute("GRANT EXECUTE ON FUNCTION allowed() TO app_user;")
    conn.execute("SELECT lo_export(456, '/tmp/backup.bin');")
    conn.execute("ALTER SYSTEM SET archive_command = 'cp %p /archive/%f';")
