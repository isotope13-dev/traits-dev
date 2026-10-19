<?php
// iconv('Windows-1252', 'UTF-8', $input);
$text = "mb_convert_encoding($input, 'UTF-8')";
function iconv_helper($input) { return $input; }
class Converter { function mb_convert_encoding($input) { return $input; } }
$result = $converter->mb_convert_encoding($input);
