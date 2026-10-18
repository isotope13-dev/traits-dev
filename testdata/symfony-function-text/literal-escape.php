<?php
function exportValue($value)
{
    $export = var_export($value, true);
    return str_replace('function () {', "function ('.') {", $export);
}
