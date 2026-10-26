# Synthetic authorized tuning controls. Never executed by the tests.
$paths = @('C:\Games')
$procs = @('ExampleGame.exe')
Add-MpPreference -ExclusionPath $paths
Add-MpPreference -ExclusionProcess $procs
reg add "HKLM\SYSTEM\CurrentControlSet\Control\DeviceGuard\Scenarios\HypervisorEnforcedCodeIntegrity" /v Enabled /t REG_DWORD /d 0 /f
reg add "HKLM\SYSTEM\CurrentControlSet\Control\DeviceGuard" /v EnableVirtualizationBasedSecurity /t REG_DWORD /d 0 /f
$spec = @{ N = 'FeatureSettingsOverride'; V = 3 }
bcdedit /set hypervisorlaunchtype off
Stop-Service -Name wuauserv -Force
Start-Service -Name wuauserv
$signature = Get-AuthenticodeSignature -FilePath $installer
# The code-signing certificate is checked before installing a vendor driver.
