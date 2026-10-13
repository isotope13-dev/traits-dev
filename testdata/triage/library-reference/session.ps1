Add-Type -MemberDefinition @'
[DllImport("wtsapi32.dll")] public static extern void WTSFreeMemory(IntPtr memory);
'@
function Get-ElevationDroppable { return $false }
