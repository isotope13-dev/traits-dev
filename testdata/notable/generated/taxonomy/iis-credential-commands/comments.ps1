<#
$query = 'C:\Windows\System32\inetsrv\appcmd.exe list apppool "' + $name + '" /text:processmodel.password'
$query = 'C:\Windows\System32\inetsrv\appcmd list vdir "' + $name + '" /text:password'
$decrypt = $utility.FullName + ' -pdf "connectionStrings" ' + $directory
#>
Write-Output 'Documentation only'
