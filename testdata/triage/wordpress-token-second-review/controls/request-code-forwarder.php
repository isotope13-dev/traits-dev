<?php
$body = http_build_query(['code' => $_POST['code'], 'user_pass' => $password]);
$response = wp_remote_post($endpoint, ['body' => $body]);
