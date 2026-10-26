[Byte[]]$PEBytes = [Byte[]][Convert]::FromBase64String($PEBytes64)
[BitConverter]::ToInt64($PEBytes, 0)
