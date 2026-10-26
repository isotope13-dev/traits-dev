# Diagnostic example: the function emits a fixed public message. The registry
# path below is documentation stored in an unused variable. There is no registry
# read, password access, encryption, process launch, network transfer, or hash dump.
function Invoke-PowerDump { Write-Output 'public diagnostic ready' }
$DocumentedRegistryPath = 'HKLM:\SYSTEM\CurrentControlSet\Control\Lsa'
Invoke-PowerDump
