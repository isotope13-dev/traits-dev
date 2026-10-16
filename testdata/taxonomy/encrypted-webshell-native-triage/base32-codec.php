<?php
function unframe($text) {
    $alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ234567';
    $bits = 0; $count = 0; $out = '';
    foreach (str_split(rtrim($text, '=')) as $char) {
        $value = strpos($alphabet, $char);
        if ($value === false) { continue; }
        $bits = ($bits << 5) | $value; $count += 5;
        if ($count >= 8) { $count -= 8; $out .= chr(($bits >> $count) & 255); }
        $bits &= (1 << $count) - 1;
    }
    return $out;
}
function frame($text) {
    $alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ234567';
    $bits = 0; $count = 0; $out = '';
    foreach (str_split($text) as $char) {
        $bits = ($bits << 8) | ord($char); $count += 8;
        while ($count >= 5) { $count -= 5; $out .= $alphabet[($bits >> $count) & 31]; }
        $bits &= (1 << $count) - 1;
    }
    if ($count) { $out .= $alphabet[($bits << (5 - $count)) & 31]; }
    return $out;
}
