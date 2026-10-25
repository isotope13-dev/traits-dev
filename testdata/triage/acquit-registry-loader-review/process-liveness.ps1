function Test-ProcessMissing {
param([string]$Name)
$p = @(Get-Process -Name $Name -ErrorAction SilentlyContinue)
return ($p.Length -eq 0)
}
