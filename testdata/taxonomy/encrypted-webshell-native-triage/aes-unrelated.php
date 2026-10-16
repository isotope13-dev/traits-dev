<?php
$unrelated = 'AES-256-CBC';
openssl_encrypt($data, 'AES-256-GCM', $key);
openssl_decrypt($data, 'AES-128-CTR', $key);
