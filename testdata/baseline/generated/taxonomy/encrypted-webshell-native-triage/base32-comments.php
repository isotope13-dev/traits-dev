<?php
function codec($text) {
    // ABCDEFGHIJKLMNOPQRSTUVWXYZ234567 strpos($text) << 5 chr($text)
    // ord($text) << 8 >> $count) & 31
    return $text;
}
