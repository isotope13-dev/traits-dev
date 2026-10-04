<?php
$trace = base64_decode($_SERVER['HTTP_X_TRACE'] ?? '');
error_log($trace);
http_response_code(404);
system('/usr/bin/true');
