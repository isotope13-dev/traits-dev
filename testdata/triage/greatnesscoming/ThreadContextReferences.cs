// Compile-only control: native API declarations, with no injection code.
using System;
using System.Runtime.InteropServices;
public static class ThreadContextReferences {
    [DllImport("kernel32.dll")]
    public static extern bool GetThreadContext(IntPtr thread, IntPtr context);
    [DllImport("kernel32.dll")]
    public static extern bool SetThreadContext(IntPtr thread, IntPtr context);
}
