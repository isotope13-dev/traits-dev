<?php
$target = '/srv/site/data.txt';
$before = filemtime($target);
$mode = fileperms($target);
file_put_contents($target, $_POST['body'] . file_get_contents($target));
touch($target, $before);
chmod($target, $mode);
