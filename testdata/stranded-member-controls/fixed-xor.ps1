function Transform { $value | ForEach-Object { $_ -BXor 0x42 } }
