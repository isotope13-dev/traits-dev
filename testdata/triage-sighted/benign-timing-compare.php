<?php
// Timing-safe comparison polyfill (synthetic negative control).
// The `^ ord(...)` operand is neutral arithmetic, not webshell obfuscation.
function timing_safe_equals($known, $user) {
    if (!is_string($known) || !is_string($user)) {
        return false;
    }
    if (strlen($known) !== strlen($user)) {
        return false;
    }
    $result = 0;
    for ($i = 0; $i < strlen($known); $i++) {
        $result |= ord($known[$i]) ^ ord($user[$i]);
    }
    return $result === 0;
}

function formatLabel($name) {
    return 'label: ' . $name;
}
