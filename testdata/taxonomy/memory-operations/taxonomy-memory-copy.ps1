param($bytes, $target)
[System.Runtime.InteropServices.Marshal]::Copy($bytes, 0, $target, $bytes.Length)
