<?php
function send_any() {
    $item = $_GET['download'] ?? '';
    if (is_file($item)) {
        header('Content-Disposition: attachment; filename="' . basename($item) . '"');
        readfile($item);
    }
}
send_any();
