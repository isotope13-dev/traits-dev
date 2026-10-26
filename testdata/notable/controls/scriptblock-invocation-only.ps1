$program='Get-Date'
[scriptblock]::Create($program).Invoke()
. ([scriptblock]::Create($program))
