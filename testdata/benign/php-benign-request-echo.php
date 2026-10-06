<?php
// Benign: request data echoed and written to a file, never executed.
$name = $_REQUEST['name'];
echo 'hello ' . htmlspecialchars($name);
file_put_contents('/tmp/greetings.log', $name . "\n", FILE_APPEND);
