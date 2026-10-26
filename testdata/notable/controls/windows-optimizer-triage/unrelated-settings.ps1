reg add "HKCU\Software\Example" /v Enabled /t REG_DWORD /d 0 /f
$spec = @{ N = 'OtherFeatureSettingsOverride'; V = 3 }
Write-Output 'OtherEnableVirtualizationBasedSecurity'
Write-Output 'OtherDeviceGuard\Scenarios\HypervisorEnforcedCodeIntegrityOther'
