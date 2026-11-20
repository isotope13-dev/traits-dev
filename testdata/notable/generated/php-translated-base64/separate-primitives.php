<?php
$translated = strtr($input, "-_", "+/");
$decoded = base64_decode($input);
$encoded = base64_encode($output);
$other = strtr($output, "ab", "cd");
// base64_decode(strtr($input, $from, $to));
/* strtr(base64_encode($output), $to, $from); */
