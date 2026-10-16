<?php
openssl_encrypt($data, 'AES-128-CBC', $key);
if ($data) { openssl_decrypt($data, 'AES-192-CBC', $key); }
