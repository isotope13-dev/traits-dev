using System;
using System.Runtime.InteropServices;

// Near miss: local-only hook check. Maps a clean ntdll copy and resolves
// one export address to compare against the loaded module. No remote
// process is opened, no remote memory is allocated or written, and no
// remote thread is created, so this must stay below suspicious.
namespace HookCheckResearch
{
    public static class Checker
    {
        public static IntPtr ResolveCleanExport(string exportName)
        {
            var mapped = DInvoke.ManualMap.Map.MapModuleToMemory("C:\\Windows\\System32\\ntdll.dll");
            object[] lookupParams = { exportName };
            IntPtr cleanAddress = (IntPtr)DInvoke.DynamicInvoke.Generic.CallMappedDLLModuleExport(
                mapped.PEINFO,
                mapped.ModuleBase,
                exportName,
                typeof(DynamicInvoke.Native.DELEGATES.GenericDelegate),
                ref lookupParams,
                false);
            Console.WriteLine("[*] resolved {0} to {1}", exportName, cleanAddress);
            return cleanAddress;
        }

        public static void ComparePrologue()
        {
            IntPtr clean = ResolveCleanExport("NtProtectVirtualMemory");
            Console.WriteLine("[*] clean address: {0}", clean);
        }
    }
}
