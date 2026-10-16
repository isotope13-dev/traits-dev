<?php
function alphabet() { return 'ABCDEFGHIJKLMNOPQRSTUVWXYZ234567'; }
function bits($text) {
    $value = strpos($text, 'a');
    $bits = ($value << 5) | 1;
    return chr($bits);
}
