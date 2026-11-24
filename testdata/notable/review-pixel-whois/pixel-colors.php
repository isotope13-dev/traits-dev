<?php
// Ordinary palette sampling with no low-bit reconstruction.
function sample($image, $x, $y) {
    $color = imagecolorat($image, $x, $y);
    return chr(($color >> 16) & 255);
}
