<?php
$owner = fileowner($path);
$account = posix_getpwuid(1000);
echo $account["name"];
