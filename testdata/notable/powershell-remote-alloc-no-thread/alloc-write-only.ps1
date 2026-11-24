# Allocates and writes a buffer in another process. No thread is started.
$hProcess = $OpenProcess.Invoke(0x001F0FFF, $false, $ProcessID)
$RemoteMemAddr = $VirtualAllocEx.Invoke($hProcess, [IntPtr]::Zero, $Length, 0x3000, 0x04)
$WriteProcessMemory.Invoke($hProcess, $RemoteMemAddr, $Data, $Data.Length, [Ref] 0) | Out-Null
Write-Output "allocated $RemoteMemAddr"
