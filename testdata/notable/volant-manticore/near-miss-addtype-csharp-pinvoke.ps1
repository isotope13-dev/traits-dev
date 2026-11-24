$sig = '[DllImport("user32.dll")] public static extern bool SetForegroundWindow(IntPtr hWnd);'
$t = Add-Type -MemberDefinition $sig -Name Win32 -Namespace Native -PassThru
$k = 0x5A
$out = foreach ($b in 1..4) { $b -bxor $k }
$out
