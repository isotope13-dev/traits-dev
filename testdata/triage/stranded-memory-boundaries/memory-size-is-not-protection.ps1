$buffer = [NativeApi]::VirtualAlloc([IntPtr]::Zero, 0x40, 0x3000, 0x04)
[NativeApi]::VirtualProtect($buffer, 0x40, 0x04, [ref]$previousProtection)
$Win32Functions.VirtualAllocEx.Invoke($process, [IntPtr]::Zero, 0x40, 0x3000, 0x04)
