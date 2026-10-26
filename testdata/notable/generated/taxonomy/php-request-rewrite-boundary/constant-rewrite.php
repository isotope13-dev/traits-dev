<?php
$target = '/srv/site/bootstrap.php';
$before = filemtime($target);
$mode = fileperms($target);
file_put_contents($target, 'replacement' . file_get_contents($target));
touch($target, $before);
chmod($target, $mode);
