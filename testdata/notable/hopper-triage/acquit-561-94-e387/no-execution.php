<?php
if (!file_exists($dest)) {
    $contents = gzdecode(base64_decode(get_option('saved_code')));
    file_put_contents($dest, $contents);
}
echo $dest;
