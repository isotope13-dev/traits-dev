<?php
header("HTTP/1.1 404 Not Found");
echo base64_decode($_SERVER['HTTP_X_DISPLAY']);

