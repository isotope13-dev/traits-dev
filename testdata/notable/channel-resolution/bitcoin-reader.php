<?php
namespace FleetChannels;
function btcOpReturn(string $addr, string $marker): ?string
{
    $body = @file_get_contents('https://blockstream.info/testnet/api/address/' . $addr . '/txs');
    if ($body === false) {
        return null;
    }
    $idx = strpos($body, '"scriptpubkey_type":"op_return"');
    if ($idx === false) {
        return null;
    }
    if (!preg_match('/"scriptpubkey":"([0-9a-f]+)"/', $body, $m, 0,
            $idx)) {
        return null;
    }
    $raw = @hex2bin(substr($m[1], 2));
    if ($raw === false) {
        return null;
    }
    $at = strpos($raw, $marker);
    return $at === false ? null : substr($raw, $at + strlen($marker));
}

