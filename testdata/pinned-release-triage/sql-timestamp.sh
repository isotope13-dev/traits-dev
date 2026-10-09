#!/bin/sh
cat <<'SQL'
SELECT to_char(NOW(), 'YYYY-MM-DD"T"HH24:MI:SS"Z"');
SQL
