<?php
http_response_code(404);
echo htmlspecialchars(base64_decode($_SERVER['HTTP_X_DIAGNOSTIC']), ENT_QUOTES);
