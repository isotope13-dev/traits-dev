$module = [System.Reflection.Assembly]::Load($bytes)
$type = $module.GetType('Example.Entry')
$method = $type.GetMethod('Run')
$method.Invoke($null, @())
