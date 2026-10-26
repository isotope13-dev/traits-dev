# Benign computed array-block controls: consecutive `@(...)` array
# subexpressions wrapping pipeline results are collection normalization, not a
# reconstruction table. Every array below is computed from cmdlet output, so
# ps1-mass-array-assignment must not fire here.
$vnetId = 'vnet-1'
$links = @($DnsLink | Where-Object { $_.vnet -eq $vnetId })
$zoneNames = @($links | ForEach-Object { ([string]$_.zone).ToLowerInvariant() })
$gateways = @($Gateway | Where-Object { $_.vnet -eq $vnetId })
$firewalls = @($Firewall | Where-Object { $_.vnet -eq $vnetId })
$bastions = @($Bastion | Where-Object { $_.vnet -eq $vnetId })
$resolvers = @($DnsResolver | Where-Object { $_.vnet -eq $vnetId })
$unavailable = @($resources | Where-Object State -EQ 'Unavailable').Count
$degraded = @($resources | Where-Object State -EQ 'Degraded').Count
