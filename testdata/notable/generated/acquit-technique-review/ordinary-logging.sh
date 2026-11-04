#!/bin/sh
mysql <<'QUERY'
SET GLOBAL general_log_file = '/var/log/database/query.log';
SET GLOBAL general_log = 1;
SELECT 'diagnostic';
SET @@global.general_log = '0';
QUERY
