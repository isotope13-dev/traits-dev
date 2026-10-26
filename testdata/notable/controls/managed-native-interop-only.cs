using System;
using System.Diagnostics;
using System.Runtime.InteropServices;

// Reading a module address and converting a native function pointer are
// ordinary interop. This control contains no status-return patch stubs.
public static class ManagedNativeInteropOnly {
    public delegate uint NtProtectVirtualMemory(IntPtr process, ref IntPtr address,
        ref IntPtr size, uint protect, ref uint previous);
    public static Delegate Resolve(IntPtr address) {
        Console.WriteLine(Process.GetCurrentProcess().MainModule.BaseAddress);
        return Marshal.GetDelegateForFunctionPointer(address, typeof(NtProtectVirtualMemory));
    }
    public static void Main() { }
}
