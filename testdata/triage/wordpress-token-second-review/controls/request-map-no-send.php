<?php
$body = http_build_query(['code' => $_POST['code'], 'user_pass' => $password]);
echo $body;
