function Transform { $I=0; $value | ForEach-Object { $_ -BXor $XORKey[$I++ % $XORKey.Length] } }
