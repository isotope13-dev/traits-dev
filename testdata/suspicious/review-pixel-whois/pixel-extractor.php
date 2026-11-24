<?php
function extract_bits($image, $width) {
    $bits = '';
    $bytes = '';
    for ($x = 0; $x < $width; $x++) {
        $color = imagecolorat($image, $x, 0);
        $bits .= (string) ($color & 1);
        if (strlen($bits) === 8) {
            $bytes .= chr(bindec($bits));
            $bits = '';
        }
    }
    return $bytes;
}
