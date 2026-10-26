Import-Module ActiveDirectory
$share = "\\corp.example\SYSVOL\corp.example\scripts"
Copy-Item -Path C:\Packages\inventory.exe -Destination "$share\inventory.exe"
New-GPO -Name Inventory
New-GPLink -Name Inventory -Target 'DC=corp,DC=example'
$taskPath = "\\corp.example\SYSVOL\corp.example\Policies\{guid}\Machine\Preferences\ScheduledTasks"
Get-ADComputer -Filter *
gpupdate /force
