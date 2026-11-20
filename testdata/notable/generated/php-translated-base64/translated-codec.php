<?php
$from = "NOPQRSTUVWXYZABCDEFGHIJKLMnopqrstuvwxyzabcdefghijklm5678901234+/";
$to = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";
$decoded = base64_decode ( strtr ( $input, $from, $to ) );
$encoded = strtr ( base64_encode ( $output ), $to, $from );
