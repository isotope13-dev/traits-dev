# Excerpt shape of the framework RPC daemon bootstrap: a default bind on
# all interfaces plus the JSON-RPC web service announcement.
opts = {
    'ServerHost' => '0.0.0.0',
    'ServerPort' => 55553,
}

$stderr.puts "[*] MSF JSON-RPC web service starting on #{opts['ServerHost']}:#{opts['ServerPort']}"
