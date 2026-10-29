$a = [System.Reflection.Assembly]::Load([IO.File]::ReadAllBytes("plugin.dll"))
$a.EntryPoint.Invoke($null, @())
