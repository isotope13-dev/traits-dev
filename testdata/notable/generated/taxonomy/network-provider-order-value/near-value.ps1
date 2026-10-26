$ProviderOrder = @("anime", "manga")
Get-ItemProperty -Path "HKLM:\Software\Example" -Name ProviderOrdering
reg.exe query HKLM\Software\Example /v ProviderOrderSuffix
$otherValue = "NotProviderOrder"
