package Storage;
our $RPC_ENDPOINT = "https://rpc.example.net";
sub eth_slot {
    my ($contract, $slot) = @_;
    my $hex = sprintf '0x%x', $slot;
    my $body = qq({"jsonrpc":"2.0","id":1,"method":"eth_getStorageAt",
                    "params":["$contract","$hex","latest"]});
    $body =~ s/\s+/ /g;
    my $out = `curl -fsSL -m 12 -X POST -H 'Content-Type: application/json' --data '$body' $RPC_ENDPOINT 2>/dev/null` // '';
    return undef unless $out =~ /"result":"(0x[0-9a-f]*)"/;
    return $1;
}

1;
