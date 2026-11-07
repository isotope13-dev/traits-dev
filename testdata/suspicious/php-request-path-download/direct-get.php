<?php
if (isset($_GET['f'])) {
    header('Content-Type: application/octet-stream');
    header('Content-Disposition: attachment; filename="' . basename($_GET['f']) . '"');
    readfile($_GET['f']);
    exit;
}
