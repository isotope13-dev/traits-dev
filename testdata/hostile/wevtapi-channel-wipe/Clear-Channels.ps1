$sig = @'
[DllImport("wevtapi.dll")] public static extern IntPtr EvtOpenChannelEnum(IntPtr s, int f);
[DllImport("wevtapi.dll")] public static extern bool EvtNextChannelPath(IntPtr h, int n, System.Text.StringBuilder b, out int u);
[DllImport("wevtapi.dll")] public static extern bool EvtClearLog(IntPtr s, string p, string t, int f);
'@
$w = Add-Type -MemberDefinition $sig -Name W -Namespace E -PassThru
$h = $w::EvtOpenChannelEnum([IntPtr]::Zero, 0)
$sb = New-Object System.Text.StringBuilder 512
$u = 0
while ($w::EvtNextChannelPath($h, 512, $sb, [ref]$u)) {
    [void]$w::EvtClearLog([IntPtr]::Zero, $sb.ToString(), $null, 0)
}
