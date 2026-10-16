<?php
$message = $_POST['message'] ?? '';
http_response_code(404);
$key = str_repeat('k', 32);
$clear = openssl_decrypt($message, 'AES-256-CBC', $key, 0, str_repeat('x', 16));
eval('return 2 + 2;');
echo $clear;
