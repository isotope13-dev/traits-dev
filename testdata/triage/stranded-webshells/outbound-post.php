<?php
$options = array('http' => array('method' => 'POST', 'content' => 'message'));
$ctx = stream_context_create($options);
$response = file_get_contents('https://example.invalid/', false, $ctx);
