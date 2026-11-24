$bytes = [System.Convert]::FromBase64String($configuredPlugin);
$plugin = [System.Reflection.Assembly]::Load($bytes);
$method = $plugin.GetType('Plugin').GetMethod('Run');
$method.Invoke($null, @());
