using System;
using System.Runtime.InteropServices;

public class ProcInfoReader
{
    [StructLayout(LayoutKind.Sequential)]
    public struct PROCESS_BASIC_INFORMATION
    {
        public IntPtr ExitStatus;
        public IntPtr PebAddress;
    }

    [DllImport("ntdll")]
    public static extern int ZwQueryInformationProcess(IntPtr hProcess, int cls, ref PROCESS_BASIC_INFORMATION pbi, uint len, ref uint ret);

    [DllImport("kernel32")]
    public static extern bool ReadProcessMemory(IntPtr hProcess, IntPtr baseAddr, byte[] buf, int size, out IntPtr read);

    public static IntPtr ReadPeb(IntPtr hProcess)
    {
        PROCESS_BASIC_INFORMATION pbi = new PROCESS_BASIC_INFORMATION();
        uint ret = 0;
        if (ZwQueryInformationProcess(hProcess, 0, ref pbi, 16, ref ret) != 0)
            return IntPtr.Zero;
        byte[] buf = new byte[8];
        IntPtr r;
        ReadProcessMemory(hProcess, pbi.PebAddress, buf, buf.Length, out r);
        return (IntPtr)BitConverter.ToInt64(buf, 0);
    }
}
