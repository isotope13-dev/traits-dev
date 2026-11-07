<?php
function custom_hmac($hash, $hexKey, $data) {
    $key = pack('H*', $hexKey);
    $ipad = $key ^ str_repeat("\x36", 64);
    $opad = $key ^ str_repeat("\x5c", 64);
    return $hash($opad . pack('H*', $hash($ipad . $data)));
}
