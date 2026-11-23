<?php
foreach ($_ENV as $key => $value) {
    if (preg_match('/PATH|LANG/i', $key)) {
        $report[$key] = $value;
    }
}
$ctx = stream_context_create(['http' => [
    'method' => 'POST', 'content' => json_encode($report)
]]);
file_get_contents('https://example.org/report', false, $ctx);
