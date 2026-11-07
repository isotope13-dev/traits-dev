<?php
$root = dirname(__FILE__);
header('Content-Description: File Transfer');
header('Content-Disposition: attachment; filename="export.bin"');
readfile($root . '/' . $_POST['name']);
