$secretNames = '^(id_rsa|id_ed25519|id_ecdsa|id_dsa)$'
if ($filename -match $secretNames) { throw 'Do not commit private keys' }
