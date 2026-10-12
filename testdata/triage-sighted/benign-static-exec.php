<?php
// Benign diagnostics page (synthetic negative control): static command,
// no availability probing, no decoding, no variable sinks.
function show_disk() {
    $output = array();
    exec('df -h', $output, $exit);
    return implode("\n", $output);
}

function show_upload_form() {
    $name = isset($_POST['name']) ? (string)$_POST['name'] : '';
    echo 'hello ' . $name;
}
