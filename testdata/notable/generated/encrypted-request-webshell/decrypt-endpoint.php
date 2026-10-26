<?php
if (!isset($_POST['packet'])) { http_response_code(404); exit; }
$key = str_repeat('k', 32);
echo openssl_decrypt(base64_decode($_POST['packet']), 'AES-256-CBC', $key, 0, str_repeat('x', 16));
