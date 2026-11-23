<?php
// An auth-path inventory sent as text, without reading credentials.
$home = getenv('HOME');
$paths = ['.composer/auth.json', '.netrc', '.docker/config.json'];
$ctx = stream_context_create(['http' => [
    'method' => 'POST', 'content' => json_encode($paths)
]]);
file_get_contents('https://example.org/inventory', false, $ctx);
