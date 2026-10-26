$query = 'C:\Tools\notappcmd.exe list apppool "' + $name + '" /text:processmodel.password'
$query = 'appcmd.exe list apppool "' + $name + '" /text:processmodel.passwordFormat'
$query = 'appcmd list vdir "' + $name + '" /text:passwordPolicy'
$decrypt = $utility.FullName + ' -pdf "connectionStringsBackup" ' + $directory
