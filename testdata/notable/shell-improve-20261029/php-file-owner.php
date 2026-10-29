<?php
$zones = file("/etc/bind/named.conf");
$account = posix_getpwuid(@fileowner("/etc/valiases/" . $domain));
echo $account["name"];
