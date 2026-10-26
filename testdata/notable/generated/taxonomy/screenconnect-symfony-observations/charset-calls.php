<?php
// Both global spellings must count as actual calls.
$a = iconv('Windows-1252', 'UTF-8', $input);
$b = \mb_convert_encoding($input, 'UTF-8', 'Windows-1252');
