<?php
error_reporting(0);
ini_set('display_errors', 'off');
$value = @file_get_contents('notes.txt');
print_r($value);
echo $value;
