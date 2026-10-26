<?php
if (hash_equals('0123456789abcdef0123456789abcdef', (string) $_POST['key'])) {
    echo 'Configuration token accepted';
}
