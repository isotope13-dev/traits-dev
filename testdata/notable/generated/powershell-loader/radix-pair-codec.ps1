function Get-Radix93Bytes {
    param(
        [string]$source,
        [string]$alphabet
    )
    if ([string]::IsNullOrEmpty($source)) { return , [byte[]]::new(0) }
    $radix = 93
    $indexMap = @{}
    for ($i = 0; $i -lt $alphabet.Length; $i++) {
        $indexMap[[int][char]$alphabet[$i]] = $i
    }
    $chars = $source.ToCharArray()
    $length = $chars.Length
    $out = New-Object System.Collections.Generic.List[byte]
    [uint32]$queue = 0
    [int]$nbits = 0
    [int]$pending = -1
    [int]$i2 = 0
    while ($i2 -lt $length) {
        if ($pending -lt 0) {
            $pending = $indexMap[[int]$chars[$i2]]
            $i2++
            continue
        }
        if ($i2 -ge $length) { break }
        $high = $indexMap[[int]$chars[$i2]]
        $low = $pending
        $pending = -1
        $i2++
        [uint32]$pairValue = [uint32]($low + ($high * $radix))
        $queue = [uint32]($queue -bor ($pairValue * [uint32](1 -shl $nbits)))
        $check = [int]($pairValue -band 8191)
        if ($check -gt 456) { $nbits += 13 } else { $nbits += 14 }
        while ($nbits -gt 7) {
            $nbits -= 8
            $out.Add([byte](($queue -band 255)))
            $queue = [uint32]($queue -shr 8)
        }
    }
    if ($pending -ge 0) {
        $tail = [uint32]($queue -bor ([uint32]$pending * [uint32](1 -shl $nbits)))
        $out.Add([byte]($tail -band 255))
    }
    return , [byte[]]$out.ToArray()
}
