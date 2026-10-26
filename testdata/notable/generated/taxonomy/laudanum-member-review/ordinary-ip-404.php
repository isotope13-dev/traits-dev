<?php
$allowedIPs = array('192.0.2.10');
$client = $_SERVER['REMOTE_ADDR'];
if (!in_array($client, $allowedIPs)) {
    header('HTTP/1.0 404 Not Found');
    die();
}
echo 'Private document';
