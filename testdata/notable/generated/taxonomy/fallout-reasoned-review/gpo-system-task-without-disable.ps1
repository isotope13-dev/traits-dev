$policy = 'Endpoint maintenance'
New-GPO -Name $policy
New-GPLink -Name $policy -Target 'DC=example,DC=test'
$destination = '\\example.test\SYSVOL\example.test\Policies\{00000000-0000-0000-0000-000000000001}\Machine\Preferences\ScheduledTasks'
$task = '<Task><Principals><Principal><UserId>NT AUTHORITY\System</UserId></Principal></Principals><Actions><Exec><Command>\\example.test\NETLOGON\agent.exe</Command></Exec></Actions></Task>'
Set-Content -LiteralPath "$destination\ScheduledTasks.xml" -Value $task
