function Decode-Buffer($encoded, $key) {
    $data = [Convert]::FromBase64String($encoded)
    for ($i = 0; $i -lt $data.Length; $i++) {
        $data[$i] = $data[$i] -bxor $key[$i % $key.Length]
    }
    return $data
}
function Call-Module($bytes) {
    $module = [System.Reflection.Assembly]::Load($bytes)
    $type = $module.GetType('Example.Entry')
    $method = $type.GetMethod('Run')
    $method.Invoke($null, @())
}
