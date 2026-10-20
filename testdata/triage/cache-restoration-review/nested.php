<?php
$target = __DIR__ . '/generated.dat';
if (!file_exists($target)) {
    $bytes = 'abc';
    $decoded = '';
    for ($i = 0; $i < strlen($bytes); $i++) {
        $decoded .= $bytes[$i] ^ 'k';
    }
    file_put_contents($target, $decoded);
}
