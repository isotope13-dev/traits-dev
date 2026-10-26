<?php
set_error_handler(function ($code, $message) { $GLOBALS['WARN'][] = $message; return true; });
$texture = ['data' => pack('C4', 0, 255, 0, 255)];
