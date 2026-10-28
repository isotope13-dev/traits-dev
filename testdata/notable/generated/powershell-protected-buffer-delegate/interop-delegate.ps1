# Calls GetTickCount64 through a delegate and marshals a small struct; no
# memory is ever made executable.
$sig = @'
[DllImport("kernel32.dll", CharSet = CharSet.Ansi)] public static extern IntPtr GetProcAddress(IntPtr h, string name);
[DllImport("kernel32.dll", CharSet = CharSet.Unicode)] public static extern IntPtr GetModuleHandle(string name);
'@
$k = Add-Type -MemberDefinition $sig -Name Native -Namespace Probe -PassThru
$fn = $k::GetProcAddress($k::GetModuleHandle("kernel32.dll"), "GetTickCount64")
$tick = [System.Runtime.InteropServices.Marshal]::GetDelegateForFunctionPointer($fn, [Func[UInt64]])
$bytes = [byte[]](1, 2, 3, 4)
$buf = [System.Runtime.InteropServices.Marshal]::AllocHGlobal($bytes.Length)
try {
    [System.Runtime.InteropServices.Marshal]::Copy($bytes, 0, $buf, $bytes.Length)
    Write-Output ("uptime ms: {0}" -f $tick.Invoke())
} finally {
    [System.Runtime.InteropServices.Marshal]::FreeHGlobal($buf)
}
