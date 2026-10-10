function Load-LocalTestLibrary {
    $PEBytes = [Convert]::FromBase64String('VEVTVA==')
    Invoke-MemoryLoadLibrary -PEBytes $PEBytes
}
