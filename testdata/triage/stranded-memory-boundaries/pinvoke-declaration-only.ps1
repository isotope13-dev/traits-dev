Add-Type -TypeDefinition @'
using System;
using System.Runtime.InteropServices;
public static class NativeApi {
    [DllImport("kernel32.dll")]
    public static extern IntPtr VirtualAlloc(IntPtr address, UIntPtr length,
        uint allocationType, uint protection);
}
'@
