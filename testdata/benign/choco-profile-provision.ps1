# Bake the default PowerShell profile into a CI runner image: install
# Chocolatey, then seed its profile module so every login gets it on PATH.
[System.Net.ServicePointManager]::SecurityProtocol = [System.Net.SecurityProtocolType]::Tls12
Invoke-WebRequest https://community.chocolatey.org/install.ps1 -UseBasicParsing | Invoke-Expression
$ChocoProfileValue = @'
$ChocolateyProfile = "$env:ChocolateyInstall\helpers\chocolateyProfile.psm1"
if (Test-Path($ChocolateyProfile)) {
  Import-Module "$ChocolateyProfile"
}
'@
$PS_PROFILE = "$PsHome\Microsoft.PowerShell_profile.ps1"
Set-Content -Path $PS_PROFILE -Value $ChocoProfileValue -Force
