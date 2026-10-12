# Ordinary policy read: a SYSVOL Policies path without GPP preference
# targeting or recursion is not a credential sweep.
$pol = '\\DC01\SYSVOL\demo.lab\Policies\{GUID}\Machine\Registry.pol'
Get-Content -Path $pol
