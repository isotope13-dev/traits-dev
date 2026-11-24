<?php
function storageRequest($address) {
    return ['method' => 'eth_getStorageAt', 'params' => [$address, '0x0', 'latest']];
}
$bytes = hex2bin('68656c6c6f');
echo $bytes;
shell_exec('/bin/sh -c ' . escapeshellarg('printf hello'));
