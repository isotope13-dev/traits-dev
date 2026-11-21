$bytes = [Convert]::FromBase64String('VEVTVA==')
[IO.File]::WriteAllBytes('plugin.dll', $bytes)
$plugin = [IO.File]::ReadAllBytes('plugin.dll')
[System.Reflection.Assembly]::Load($plugin)
